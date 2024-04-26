eur_kr =  open("./tpss_bcycl_od_statnhm_20240421.csv", mode="r", encoding="euc-kr")
utf_8 = open("./20240421.csv", mode="w")

for line in eur_kr:
    utf_8.write(line.encode("utf-8"))
    
eur_kr.close()
utf_8.close()
    