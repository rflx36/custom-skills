"""Material-group parser; usable without Blender."""
import re

MATERIALS = ('Concrete', 'Ground', 'Leather', 'Metal', 'Pavement', 'Plastic',
             'Rock', 'Rubber', 'Rust', 'Stone', 'Wood', 'Glass', 'Color')
_CANONICAL = {name.lower(): name for name in MATERIALS}
_NAME = re.compile(r'^([A-Za-z]+)([0-9]*)_(.+)$')


def parse_name(name):
    """Return group information; accept legacy unnumbered known prefixes.

    Decimal strings avoid imposing an arbitrary integer-size limit on groups.
    """
    match = _NAME.fullmatch(name)
    if not match or not match[3].strip():
        raise ValueError(f'Expected MaterialNumber_ObjectName: {name}')
    material = _CANONICAL.get(match[1].lower())
    if material is None:
        raise ValueError(f'Unknown material prefix: {name}')
    number = match[2]
    if number and number[0] == '0':
        raise ValueError(f'Group must be positive without leading zeros: {name}')
    group = number or '1'
    canonical = f'{material}{group}_{match[3]}'
    return dict(material=material, group=group, description=match[3],
                canonical=canonical, legacy=name != canonical)
