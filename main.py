from src.timeconstraineddict import TimeConstrainedDict as tdict

def run():
    d = tdict()
    d["key"] = "value"
    d["key2"] = "value2", 20, 2
    d["key3"] = {"value3": 20}, 20
    d["key4"] = "hej", 20
    print(d)
    #print({**d})

if __name__ == "__main__":
    run()
