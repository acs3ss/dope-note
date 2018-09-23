import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict

dependencies = [
    'you-get>=0.4.1099',
    'python-rake>=1.4.5'
]

# here, if a dependency is not met, a DistributionNotFound or VersionConflict
# exception is thrown. 
pkg_resources.require(dependencies)
