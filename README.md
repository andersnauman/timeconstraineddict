## Time Constrained Dictionary
### Description
Creates a dictionary where the key/value will expire after the set timelimit (default 60 sec).

### Usage
```
from timeconstraineddict import TimeConstrainedDict as tdict

# Set value to expire in 2 seconds
d = tdict()
d["key"] = "value", 2

# Set the tuple ("value", 20) to expire in 2 seconds
d = tdict()
d["key"] = "value", 20, 2

# Set the default expire time to 5 minutes
d = tdict(300)
d["key"] = "value"
```