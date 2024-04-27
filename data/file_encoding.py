
def changeSave(euc_kr, utf_8):
    content = euc_kr.read()
    utf_8.write(content)
    euc_kr.close()
    utf_8.close()
    
# changeSave(
#     open("./tpss_bcycl_od_statnhm_20240421.csv", mode="r", encoding="euc-kr"),
#     open("./20240421.csv",encoding='utf-8', mode="w")
# )

changeSave(
    open("./stops_euc_kr.csv", mode="r", encoding="euc-kr"),
    open("./stops.csv",encoding='utf-8', mode="w")
)