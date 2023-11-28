from req_lib import ReqLib

if __name__ == "__main__":
    req_lib = ReqLib()

    req = req_lib.getJSON(
        req_lib.configs.MEMBERS_FULL,
        group="Department 25500 Faculty",
    )

    print(req)