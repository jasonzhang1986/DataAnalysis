import csv


def write_csv(result):
    with open('douban_movie1.csv', 'a', encoding='gb18030', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(result)


result_title = ['名字', '导演', '主演', '年份', '时长', '国家', '类型', '评分']
write_csv(result_title)

linNo = 0
with open('douban_movie_clean.txt', 'r', encoding='UTF-8') as f:
    for line in f.readlines():
        linNo += 1
        if linNo==1:
            continue
        data = line.split('^')
        print(data)
        title = data[1]
        director = data[5]
        actor = data[7]
        showtime = data[11]
        lenth = data[12]
        district = data[9]
        category = data[8]
        rate = data[4]
        result = [title,director,actor, showtime, lenth,district, category, rate]
        print(result)
        write_csv(result)
