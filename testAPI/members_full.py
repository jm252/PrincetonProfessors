from req_lib import ReqLib 
import datetime

if __name__ == "__main__":
    req_lib = ReqLib()
    today = datetime.datetime.today()
    # year = str(today.year)

    req = req_lib.getJSON(
        req_lib.configs.MEMBERS_FULL,
        group="Department 25500 Faculty",
    )
    print(req)