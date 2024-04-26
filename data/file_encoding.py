eur_kr =  open("./tpss_bcycl_od_statnhm_20240421.csv", mode="r", encoding="euc-kr")
utf_8 = open("./20240421.csv",encoding='utf-8', mode="w")

content = eur_kr.read()
utf_8.write(content)

eur_kr.close()
utf_8.close()
    