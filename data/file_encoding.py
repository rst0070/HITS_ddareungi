
def changeSave(euc_kr, utf_8):
    content = euc_kr.read()
    utf_8.write(content)
    euc_kr.close()
    utf_8.close()
    
# changeSave(
#     open("./raw_data/tpss_bcycl_od_statnhm_20240503.csv", mode="r", encoding="euc-kr"),
#     open("./encoded_data/20240503.csv",encoding='utf-8', mode="w")
# )

changeSave(
    open("./raw_data/stops_euc_kr.csv", mode="r", encoding="euc-kr"),
    open("./encoded_data/stops.csv",encoding='utf-8', mode="w")
)