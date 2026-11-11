-- Reusable helper for Studio execute_luau or a temporary ModuleScript.
-- No changes occur on require. Caller chooses the exact source and integration.
local R = {}
local roles = {rust="Rust", metal="Metal", plastic="Plastic", wood="Wood"}
local fromMaterial = {
 [Enum.Material.CorrodedMetal]="Rust",
 [Enum.Material.Metal]="Metal",
 [Enum.Material.DiamondPlate]="Metal",
 [Enum.Material.Plastic]="Plastic",
 [Enum.Material.SmoothPlastic]="Plastic",
 [Enum.Material.Wood]="Wood",
 [Enum.Material.WoodPlanks]="Wood",
}

-- The role selects the palette; the group selects an independent draw.
function R.roleAndGroupFromName(name)
 -- Blender uses both "_" and "." separators; stop at whichever occurs first.
 local token = tostring(name):match("^([^_%.]+)") or ""
 token = token:match("^%s*(.-)%s*$")
 local base,suffix = token:lower():match("^([a-z]+)([2345]?)$")
 local role = base and roles[base] or nil
 if not role then return nil,nil end
 return role, role .. suffix
end

function R.roleFromName(name)
 local role = R.roleAndGroupFromName(name)
 return role
end

function R.groupFromName(name)
 local _,group = R.roleAndGroupFromName(name)
 return group
end

function R.originalName(name)
 local result = tostring(name)
 local separator = result:find("[_%.]")
 if R.roleFromName(result) and separator then
  result = result:sub(separator + 1)
 end
 return result:gsub("%.%d+$", ""):gsub("_%d+$", "")
end

local function visibleParts(model)
 local list = {}
 for _,p in ipairs(model:GetDescendants()) do
  if p:IsA("BasePart") and p.Transparency < 1 then
   table.insert(list, p)
  end
 end
 return list
end

-- Reuse the provider's weighted looks; assign once per group, without reparenting geometry.
function R.applyGroupedMaterials(model, materials, rng)
 assert(materials and type(materials.Looks)=="table", "Use the existing scrap material provider")
 rng = rng or Random.new()
 if materials.ensureVariants then materials.ensureVariants() end
 local groups,keys = {},{}
 local contents = model:FindFirstChild("Scraps")
 for _,p in ipairs(visibleParts(model)) do
  if contents and p:IsDescendantOf(contents) then continue end
  local role,group = R.roleAndGroupFromName(p.Name)
  if not role then
   role = roles[tostring(p:GetAttribute("ScrapRole")):lower()]
   if role then
    local groupRole,existing = R.roleAndGroupFromName(p:GetAttribute("ScrapMaterialGroup") or role)
    group = groupRole==role and existing or role
   end
  end
  if role then
   p:SetAttribute("ScrapRole",role)
   p:SetAttribute("ScrapMaterialGroup",group)
   if not groups[group] then
    groups[group] = {role=role,parts={}}
    table.insert(keys,group)
   end
   table.insert(groups[group].parts,p)
  end
 end
 table.sort(keys)
 local chosen = {}
 for _,group in ipairs(keys) do
  local entry = groups[group]
  local looks = assert(materials.Looks[entry.role],"Missing material palette: "..entry.role)
  local total = 0
  for _,look in ipairs(looks) do total += math.max(look.Weight or 0,0) end
  assert(total>0,"No positive material weights for "..entry.role)
  local draw = rng:NextNumber(0,total)
  local selected
  for _,look in ipairs(looks) do
   if (look.Weight or 0)>0 then
    selected=look
    draw-=look.Weight
    if draw<=0 then break end
   end
  end
  assert(selected and #selected.Colors>0,"Material look needs a color palette")
  chosen[group]=selected
  model:SetAttribute("Look_"..group,selected.Name)
  for _,p in ipairs(entry.parts) do
   p.Material=selected.Material
   p.MaterialVariant=selected.Variant
   p.Color=selected.Colors[rng:NextInteger(1,#selected.Colors)]
   p:SetAttribute("ScrapLook",selected.Name)
  end
 end
 return chosen
end

function R.stage(source, options)
 assert(source and source:IsA("Model"), "Choose the exact imported Model")
 options = options or {}
 local factor = options.scale or 1
 assert(type(factor)=="number" and factor > 0, "Scale must be positive")
 local sourceFrame = options.sourceReference or source:GetPivot()
 local targetFrame = options.targetReference or CFrame.identity
 local originals = {}
 if options.originalPrefab then
  for _,p in ipairs(visibleParts(options.originalPrefab)) do
   originals[p.Name] = originals[p.Name] or p
  end
 end
 local prefab = Instance.new("Model")
 prefab.Name = "Prefab"
 local report = {parts=0, roles={Rust=0,Metal=0,Plastic=0,Wood=0}, groups={}, untagged={}}
 local ok,err = pcall(function()
  for _,p in ipairs(visibleParts(source)) do
   local clone = p:Clone()
   -- Static structural rework does not copy scripts or external physics joints.
   for _,child in ipairs(clone:GetDescendants()) do
    if child:IsA("LuaSourceContainer") or child:IsA("Constraint") or child:IsA("JointInstance") or child:IsA("WeldConstraint") then
     child:Destroy()
    end
   end
   clone.Size = p.Size * factor
   local rel = sourceFrame:ToObjectSpace(p.CFrame)
   clone.CFrame = targetFrame * (CFrame.new(rel.Position * factor) * rel.Rotation)
   clone.Anchored = true
   clone:SetAttribute("ImportedObjectName", p.Name)
   local original = originals[R.originalName(p.Name)]
   if original then
    clone.Material = original.Material
    clone.MaterialVariant = original.MaterialVariant
    clone.Color = original.Color
    clone.Reflectance = original.Reflectance
   end
   local role,group = R.roleAndGroupFromName(p.Name)
   if not role then
    local inherited = p:GetAttribute("ScrapRole")
    role = inherited and roles[tostring(inherited):lower()] or nil
    if role then
     local groupRole,inheritedGroup = R.roleAndGroupFromName(p:GetAttribute("ScrapMaterialGroup") or role)
     group = groupRole==role and inheritedGroup or role
    end
   end
   if not role and original then
    role,group = R.roleAndGroupFromName(original.Name)
    if not role then
     role = roles[tostring(original:GetAttribute("ScrapRole")):lower()] or fromMaterial[original.Material]
     if role then
      local groupRole,inheritedGroup = R.roleAndGroupFromName(original:GetAttribute("ScrapMaterialGroup") or role)
      group = groupRole==role and inheritedGroup or role
     end
    end
   end
   clone:SetAttribute("ScrapRole", role)
   clone:SetAttribute("ScrapMaterialGroup", group)
   if role then
    report.roles[role] += 1
    report.groups[group] = (report.groups[group] or 0) + 1
   else table.insert(report.untagged, p.Name) end
   clone.Parent = prefab
   report.parts += 1
  end
  if options.markers then options.markers:Clone().Parent = prefab end
  prefab.WorldPivot = CFrame.identity
  if options.materials then
   R.applyGroupedMaterials(prefab, options.materials, options.rng or Random.new())
  end
 end)
 if not ok then prefab:Destroy() error(err, 0) end
 return prefab, report
end

function R.validate(prefab, expectedParts, materials)
 local count = 0
 local groupLooks = {}
 for _,p in ipairs(visibleParts(prefab)) do
  count += 1
  assert(p.Anchored, "Unanchored structural part: "..p.Name)
  if p:IsA("MeshPart") then
   assert(p.MeshId ~= "" and p.MeshContent.SourceType == Enum.ContentSourceType.Uri,
    "Mesh is not a persistent imported asset: "..p.Name)
  end
  local role = p:GetAttribute("ScrapRole")
  if role then
   assert(roles[role:lower()]==role, "Invalid ScrapRole: "..tostring(role))
   local namedRole,namedGroup = R.roleAndGroupFromName(p.Name)
   local group = p:GetAttribute("ScrapMaterialGroup") or role
   local groupRole,canonical = R.roleAndGroupFromName(group)
   assert(groupRole==role and canonical==group, "Invalid material group: "..tostring(group))
   if namedRole then
    assert(role==namedRole and group==namedGroup,"Name-based material group was lost: "..p.Name)
   end
   if groupLooks[group] then
    assert(groupLooks[group].material==p.Material and groupLooks[group].variant==p.MaterialVariant,
     "Material look differs within group: "..group)
   else
    groupLooks[group]={material=p.Material,variant=p.MaterialVariant}
   end
   if materials then
    assert(materials.Looks[role] and #materials.Looks[role] > 0, "Missing role variants: "..role)
    local recognized = false
    for _,look in ipairs(materials.Looks[role]) do
     if p.Material == look.Material and p.MaterialVariant == look.Variant then
      recognized = true break
     end
    end
    assert(recognized, "Material look was not assigned: "..p.Name)
   end
  end
 end
 assert(count > 0, "Empty prefab")
 if expectedParts then assert(count==expectedParts, "Visible geometry count changed") end
 return count
end

-- Call only AFTER prefab, generator, gallery, scale, and contents validation.
function R.cleanupReference(source, backupFolder, committedPrefab)
 assert(source and source:IsA("Model"), "Retain the exact source instance")
 assert(source:IsDescendantOf(workspace), "Cleanup targets only the processed Workspace import")
 assert(committedPrefab and committedPrefab:IsDescendantOf(game:GetService("ServerStorage")), "Commit the replacement first")
 assert(source ~= committedPrefab and not committedPrefab:IsDescendantOf(source), "Source and destination overlap")
 assert(backupFolder and backupFolder:IsDescendantOf(game:GetService("ServerStorage")), "Backup must be outside Workspace")
 local library = game:GetService("ServerStorage"):FindFirstChild("Structures")
 assert(not library or (backupFolder ~= library and not backupFolder:IsDescendantOf(library)), "Keep backups outside the live Structures library")
 local clone = source:Clone()
 assert(clone, "Reference backup failed")
 clone.Name = source.Name .. "_ImportedReferenceBackup"
 clone.Parent = backupFolder
 source:Destroy()
 return clone
end
return R

