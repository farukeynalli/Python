from flask import Flask, render_template, url_for, redirect, request
import sqlite3
import requests
from bs4 import BeautifulSoup
import lxml
import sqlite3

app = Flask(__name__)


def n11_scrap():
    # conn = sqlite3.connect("student.db")
    # c = conn.cursor()
    for sayfaNo in range(1, 10):
        url = "https://www.n11.com/bilgisayar/dizustu-bilgisayar?pg={}".format(sayfaNo)
        r = requests.get(url)
        print(url)
        soup = BeautifulSoup(r.content, "lxml")
        urunler = soup.find_all("li", attrs={"class": "column"})
        for urun in urunler:
            urunAdi = urun.a.get("title")
            urunLink = urun.a.get("href")
            print(urunAdi)
            try:
                urun_price = urun.find("span", attrs={"class": "newPrice cPoint priceEventClick"}).text
                urun_price = urun_price.strip().replace(" TL", "")
                urun_price = urun_price.replace(".", "")
                if "," in urun_price:
                    urun_price = urun_price[0:len(urun_price) - 3]
                    sonPrice = int(urun_price)
                    print("Fiyat -> " + urun_price)
            except Exception:
                print("Fiyat Bulunamadı")

            photo = urun.find("img", {"class": "lazy cardImage"}).get("data-src")
            print(photo)
            try:
                urun_r = requests.get(urunLink)
            except Exception:
                print("Ürün detayı bulunamadı")

            urun_soup = BeautifulSoup(urun_r.content, "lxml")

            try:
                urun_rating = urun_soup.find("strong", attrs={"class": "ratingScore"}).text
                if "," in urun_rating:
                    urun_rating = urun_rating.replace(",", ".")
                    print("Rating -> " + urun_rating)
                else:
                    print(urun_rating)
            except Exception:
                print("rating Bulunamadı")

            store = "n11"
            ozellikler = urun_soup.find_all("li", attrs={"class": "unf-prop-list-item"})
            for ozelllik in ozellikler:
                urun_label = ozelllik.find("p", attrs={"class": "unf-prop-list-title"}).text
                try:
                    urun_data = ozelllik.find("p", attrs={"class": "unf-prop-list-prop"}).text

                    if "Ekran Boyutu" in urun_label:
                        ekranBoyutu = urun_data
                        ekranBoyutu = ekranBoyutu.replace("\"", "")
                    elif "İşlemci Modeli" in urun_label:
                        islemciNesli = urun_data
                    elif "İşlemci" in urun_label:
                        islemciTipi = urun_data
                    elif "Bellek Kapasitesi" in urun_label:
                        ram = urun_data
                    elif "İşletim Sistemi" in urun_label:
                        isletimSistemi = urun_data
                    elif "Marka" in urun_label:
                        marka = urun_data
                        marka = marka.strip()
                        marka = marka.capitalize()
                    elif "Model" in urun_label:
                        model = urun_data
                        if model == "Huawei":
                            model = "-"

                except Exception:
                    urun_data = ozelllik.find("span", attrs={"class": "data"}).find("span").text
                # print("{} : {}".format(urun_label,urun_data))
            print(marka)
            c.execute(
                """ INSERT INTO Ozellikler("satici","marka","model","urunAdi","urunPrice","ram","Ekran","image","isletimSistemi","islemciNesli","islemciTipi","rating","link") VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (store, marka, model, urunAdi, sonPrice, ram, ekranBoyutu, photo, isletimSistemi, islemciNesli,
                 islemciTipi,
                 urun_rating, urunLink,))
            conn.commit()
            print("*_-_* " * 10 + "\n")


def trendyol_Scrap():
    # conn = sqlite3.connect("student.db")
    # c = conn.cursor()

    for sayfaNo in range(1, 10):
        url = "https://www.trendyol.com/laptop-x-c103108?pi=" + str(sayfaNo)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "lxml")
        urunler = soup.find_all("div", attrs={"class": "p-card-wrppr with-campaign-view"})
        for urun in urunler:
            marka = urun.find("span", attrs={"class": "prdct-desc-cntnr-ttl"}).text
            marka = marka.capitalize()
            print(marka)
            linkbasi = "https://www.trendyol.com"
            linksonu = urun.a.get("href")
            sonlink = linkbasi + linksonu
            star = 0
            try:
                rating = urun.find("div", attrs={"class": "ratings"})
                rating2 = rating.find_all("div", attrs={"class": "star-w"})
                for i in rating2:
                    rating3 = i.find_all("div", attrs={"class": "full"})
                    rating3 = str(rating3)
                    # print(rating3)
                    sayilar = rating3[32:35]
                    # sayilar = int(sayilar)
                    # print(sayilar)
                    if sayilar == "100":
                        sayilar = int(sayilar)
                        star += sayilar

                    else:
                        if "%" in sayilar:
                            sayilar = sayilar.replace("%", " ")
                            sayilar = sayilar.replace(";", "")
                            sayilar = int(sayilar)
                            star += sayilar
                star = star / 100
                sonrate = float(star)

            except Exception:
                sonrate = 0.0

            print("rating ->", sonrate)
            print(sonlink)

            try:
                urun_r = requests.get(sonlink)
            except Exception:
                print("Ürün detayı bulunamadı")

            urun_soup = BeautifulSoup(urun_r.content, "lxml")
            # product_img = urun_soup.find("img",attrs={"class":"product-stamp ll cf"}).get("src")
            # print(product_img)
            photo = urun_soup.find_all("img")
            img_trend = []
            for foto in photo:
                img_trend.append(foto.get("src"))
            print(img_trend[1])

            product_name = urun_soup.find("h1", attrs={"class": "pr-new-br"}).text
            print(product_name)
            try:
                urun_price = urun_soup.find("span", attrs={"class": "prc-dsc"}).text
                print(urun_price + " başta")
                urun_price = urun_price.rstrip(" TL")
                urun_price = urun_price.replace(".", "")
                if "," in urun_price:
                    urun_price = urun_price[0:len(urun_price) - 3]
                    sonPrice = int(urun_price)
                    print(urun_price + "ifin içi")
                else:
                    sonPrice = int(urun_price)
                    print(urun_price + "else içi")
                print("Fiyat -> " + urun_price)
            except Exception:
                print("Fiyat Bulunamadı")

            model = urun_soup.find("h1", {"class": "pr-new-br"}).span.text
            tamAd = list(str(model).split())

            if (marka == "Monster"):
                model_no = tamAd[2]
            elif (marka == "Casper"):
                model_no = tamAd[1]
                if (model_no == "Intel"):
                    model_no = tamAd[len(tamAd) - 1]
            elif (marka == "Msi"):
                model_no = tamAd[3]
            elif (marka == "Game garaj"):
                model_no = tamAd[len(tamAd) - 2]
            else:
                model_no = tamAd[len(tamAd) - 1]
                if (model_no == "Yıl") or (model_no == "Bilgisayar"):
                    model_no = "-"

            store = "Trendyol"
            ozellikler = urun_soup.find_all("li", attrs={"class": "detail-attr-item"})
            for ozelllik in ozellikler:
                urun_label = ozelllik.find("span").text
                try:
                    urun_data = ozelllik.find("b").text

                    if "Ekran Boyutu" in urun_label:
                        ekranBoyutu = urun_data
                        ekranBoyutu = ekranBoyutu.split()
                    elif "İşlemci Nesli" in urun_label:
                        islemciNesli = urun_data
                    elif "İşlemci Tipi" in urun_label:
                        islemciTipi = urun_data
                    elif "Ram (Sistem Belleği)" == urun_label:
                        ram = urun_data
                    elif "İşletim Sistemi" in urun_label:
                        isletimSistemi = urun_data

                except Exception:
                    urun_data = ozelllik.find("span").text
                # print("{} : {}".format(urun_label, urun_data))

            c.execute(
                """ INSERT INTO Ozellikler("satici","marka","model","urunAdi","urunPrice","ram","Ekran","image","isletimSistemi","islemciNesli","islemciTipi","rating","link") VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (store, marka, model_no, product_name, sonPrice, ram, ekranBoyutu[0], img_trend[1], isletimSistemi,
                 islemciNesli,
                 islemciTipi, sonrate, sonlink,))
            conn.commit()
            print("*_-_* " * 10 + "\n")


def vatan_Scrap():
    # conn = sqlite3.connect("student.db")
    # c = conn.cursor()
    for sayfaNo in range(1, 10):
        url = "https://www.vatanbilgisayar.com/notebook/?page=" + str(sayfaNo)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "lxml")
        urunler = soup.find_all("div", attrs={"class": "product-list product-list--list-page"})
        for urun in urunler:
            product_title = urun.find("div", attrs={"class": "product-list__product-name"}).h3.text
            product_title2 = urun.find("div", attrs={"class": "product-list__product-name"}).h3.text
            product_title2 = list(product_title2.split())
            marka = product_title2[0]
            marka = marka.capitalize()
            print(marka)
            print(product_title)
            linkbasi = "https://www.vatanbilgisayar.com"
            linksonu = urun.a.get("href")
            sonlink = linkbasi + linksonu
            # print(sonlink)
            try:
                urun_r = requests.get(sonlink)
            except Exception:
                print("Ürün detayı bulunamadı")

            urun_soup = BeautifulSoup(urun_r.content, "lxml")
            try:
                urun_price = urun_soup.find("div",
                                            attrs={"class": "product-list__cost product-list__description"}).span.text
                urun_price = urun_price.replace(".", "")
                sonPrice = int(urun_price)
                print("Fiyat -> " + urun_price + " TL")
            except Exception:
                sonPrice = 0
                print("Fiyat Bulunamadı")

            try:
                urun_rating = urun_soup.find("strong", attrs={"id": "averageRankNum"}).text
                print("Rating -> " + urun_rating)

            except Exception:
                print("rating Bulunamadı")
            store = "Vatan Bilgisayar"

            photo = urun_soup.find("a", {"data-fancybox": "images"}).get("href")
            print(photo)

            model = urun_soup.find("div", {"class": "product-list__product-code pull-left product-id"}).get(
                "data-productcode")
            print(model)

            ozellikler = urun_soup.find_all("tr", attrs={"data-count": "0"})
            for ozelllik in ozellikler:
                urun_label = ozelllik.td.text
                try:
                    urun_data = ozelllik.p.text

                    if "Ekran Boyutu" in urun_label:
                        ekranBoyutu = urun_data
                        ekranBoyutu = list(ekranBoyutu.split())
                    elif "İşlemci Nesli" in urun_label:
                        islemciNesli = urun_data
                    elif "İşlemci Teknolojisi" in urun_label:
                        islemciTipi = urun_data
                    elif "Ram (Sistem Belleği)" in urun_label:
                        ram = urun_data
                    elif "İşletim Sistemi" in urun_label:
                        isletimSistemi = urun_data
                except Exception:
                    urun_data = ozelllik.p.text
            c.execute(
                """ INSERT INTO Ozellikler("satici","marka","model","urunAdi","urunPrice","ram","Ekran","image","isletimSistemi","islemciNesli","islemciTipi","rating","link") VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (store, marka, model, product_title, sonPrice, ram, ekranBoyutu[0], photo, isletimSistemi, islemciNesli,
                 islemciTipi, urun_rating, sonlink,))
            conn.commit()
            # print("{} : {}".format(urun_label,urun_data))
            print("*_-_* " * 10 + "\n")


def hepsiburada_Scrap():
    for sayfaNo in range(1, 10):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.117'}
        url = "https://www.hepsiburada.com/laptop-notebook-dizustu-bilgisayarlar-c-98?sayfa=" + str(sayfaNo)
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, "lxml")
        urunler = soup.find_all("li", attrs={"class": "productListContent-zAP0Y5msy8OHn5z7T_K_"})
        for urun in urunler:
            product_title = urun.a.get("title")
            product_title2 = list(product_title.split())
            marka = product_title2[0]
            marka = marka.capitalize()

            # print(product_title2[0])
            print(product_title)
            linkbasi = "https://www.hepsiburada.com"
            linksonu = urun.a.get("href")
            sonlink = linkbasi + linksonu
            # print(sonlink)
            photo = urun.find("div", {"data-test-id": "product-image-image"}).img.get("src")
            try:
                urun_r = requests.get(sonlink, headers=headers)
            except Exception:
                print("Ürün detayı bulunamadı")

            urun_soup = BeautifulSoup(urun_r.content, "lxml")
            store = "Hepsiburada"
            try:
                original_price = urun_soup.find("span", attrs={
                    "data-bind": "markupText:'currentPriceBeforePoint'"}).text
                original_price = original_price.replace(".", "")
                original_price = int(original_price)
                print("Fiyat -> ", original_price)

            except Exception:
                original_price = 0
                print("Fiyat Bulunamadı")

            try:
                urun_rating = urun_soup.find("span", attrs={"class": "rating-star"}).text
                urun_rating = urun_rating.strip().replace(",", ".")
                print("Rating -> " + urun_rating)

            except Exception:
                print("rating Bulunamadı")

            model = urun_soup.find("h1", {"itemprop": "name"}).text
            model = list(model.split())

            if (model[0] == "Monster") or (model[0] == "MSI"):
                model_no = model[3]
            elif (model[0] == "Asus"):
                model_no = sonlink.split("-")
                model_no = model_no[len(model_no) - 1]
            elif (model[0] == "Casper"):
                model_no = model[2]
            elif (model[0] == "Huawei"):
                model_no = "-"
            else:
                model_no = model[len(model) - 1]
                if (model_no == "Bilgisayar") or (model_no == "Yıl") or (model_no == "Dos") or (model_no == "Notebook"):
                    model_no = "-"
            print(model_no)

            ozellikler = urun_soup.find("table", attrs={"class": "data-list tech-spec"})
            ozellikler1 = ozellikler.find_all("tr")

            for ozelllik in ozellikler1:

                urun_label = ozelllik.th.text
                try:
                    urun_data = ozelllik.td.text
                    urun_data = urun_data.strip()
                    if "Ekran Boyutu" in urun_label:
                        ekranBoyutu = urun_data
                        ekranBoyutu = ekranBoyutu.split()
                    elif "İşlemci Nesli" in urun_label:
                        islemciNesli = urun_data

                    elif "İşlemci Tipi" in urun_label:
                        islemciTipi = urun_data
                    elif "Ram (Sistem Belleği)" in urun_label:
                        ram = urun_data
                    elif "İşletim Sistemi" in urun_label:
                        isletimSistemi = urun_data
                    # elif "Ram (Sistem Belleği)" in urun_label:
                    #     ram = urun_data
                except Exception:
                    urun_data = ozelllik.td.text

            c.execute(
                """ INSERT INTO Ozellikler("satici","marka","model","urunAdi","urunPrice","ram","Ekran","image","isletimSistemi","islemciNesli","islemciTipi","rating","link") VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (store, marka, model_no, product_title, original_price, ram, ekranBoyutu[0], photo, isletimSistemi,
                 islemciNesli,
                 islemciTipi, urun_rating, sonlink,))
            conn.commit()
            # print("{} : {}".format(urun_label.strip().replace("\n",""),urun_data.strip().replace("\n","")))

            print("*_-_* " * 10)


@app.route('/rating')
def rating():
    con = sqlite3.connect("student.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Ozellikler ORDER BY rating DESC")
    tamamı = cur.fetchall()
    kur = con.cursor()
    kur.execute("SELECT DISTINCT marka FROM Ozellikler")
    markalar = kur.fetchall()
    return render_template("rating.html", tamamı=tamamı, markalar=markalar)


@app.route('/azalan')
def azalan():
    con = sqlite3.connect("student.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * from Ozellikler ORDER BY urunPrice DESC")
    tamamı = cur.fetchall()
    kur = con.cursor()
    kur.execute("SELECT DISTINCT marka FROM Ozellikler")
    markalar = kur.fetchall()
    return render_template("azalan.html", tamamı=tamamı, markalar=markalar)


@app.route('/artan')
def artan():
    con = sqlite3.connect("student.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * from Ozellikler ORDER BY urunPrice ASC")
    tamamı = cur.fetchall()
    kur = con.cursor()
    kur.execute("SELECT DISTINCT marka FROM Ozellikler")
    markalar = kur.fetchall()
    return render_template("artan.html", tamamı=tamamı, markalar=markalar)


@app.route('/laptop/<string:marks>')
def laptop(marks):
    con = sqlite3.connect("student.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * from Ozellikler ")
    tamamı = cur.fetchall()

    kur = con.cursor()
    kur.execute("SELECT DISTINCT marka FROM Ozellikler")
    markalar = kur.fetchall()

    return render_template("laptop.html", tamamı=tamamı, markalar=markalar, marks=marks)


@app.route('/laptop/<string:marks>/artan')
def laptop_Artan(marks):
    con = sqlite3.connect("student.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * from Ozellikler ")
    tamamı = cur.fetchall()

    kur = con.cursor()
    kur.execute("SELECT DISTINCT marka FROM Ozellikler")
    markalar = kur.fetchall()

    zur = con.cursor()
    zur.execute("SELECT * FROM Ozellikler ORDER BY urunPrice ASC")
    artan = zur.fetchall()

    return render_template("laptop_Artan.html", tamamı=tamamı, markalar=markalar, artan=artan, marks=marks)


@app.route('/laptop/<string:marks>/rating')
def laptop_Rating(marks):
    con = sqlite3.connect("student.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * from Ozellikler ")
    tamamı = cur.fetchall()

    kur = con.cursor()
    kur.execute("SELECT DISTINCT marka FROM Ozellikler")
    markalar = kur.fetchall()

    zur = con.cursor()
    zur.execute("SELECT * FROM Ozellikler ORDER BY rating DESC")
    rating = zur.fetchall()

    return render_template("laptop_Rating.html", tamamı=tamamı, markalar=markalar, rating=rating, marks=marks)


@app.route('/laptop/<string:marks>/azalan')
def laptop_Azalan(marks):
    con = sqlite3.connect("student.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * from Ozellikler ")
    tamamı = cur.fetchall()

    kur = con.cursor()
    kur.execute("SELECT DISTINCT marka FROM Ozellikler")
    markalar = kur.fetchall()

    zur = con.cursor()
    zur.execute("SELECT * FROM Ozellikler ORDER BY urunPrice DESC")
    azalan = zur.fetchall()

    return render_template("laptop_Azalan.html", tamamı=tamamı, markalar=markalar, azalan=azalan, marks=marks)


@app.route('/')
def hello_world():
    con = sqlite3.connect("student.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Ozellikler")
    pcTamAd = cur.fetchall()
    kur = con.cursor()
    kur.execute("SELECT DISTINCT marka FROM Ozellikler")
    markalar = kur.fetchall()
    return render_template("index.html", pcTamAd=pcTamAd, markalar=markalar)


@app.route('/view')
def view():
    con = sqlite3.connect("student.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Ozellikler")
    rows = cur.fetchall()
    return render_template("view.html", rows=rows)


@app.route('/delete/<id>')
def delete(id):
    con = sqlite3.connect("student.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("DELETE FROM Ozellikler WHERE ProductID = {}".format(id))
    con.commit()

    kur = con.cursor()
    kur.execute("SELECT * FROM Ozellikler")
    rows = kur.fetchall()

    return render_template("admin.html", rows=rows)


def duplicate_Control():
    c.execute(
        "DELETE FROM Ozellikler WHERE ProductID NOT IN(SELECT MAX(ProductID)FROM Ozellikler GROUP BY model,satici);")
    conn.commit()


@app.route('/Details/<id>')
def Details(id):
    con = sqlite3.connect("student.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Ozellikler where ProductID ={}".format(id))
    rows = cur.fetchall()
    return render_template("Details.html", rows=rows)


@app.route('/admin')
def admin():
    con = sqlite3.connect("student.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Ozellikler")
    rows = cur.fetchall()
    return render_template("admin.html", rows=rows)


@app.route('/duplicate')
def duplicate():
    con = sqlite3.connect("student.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(
        "SELECT * FROM Ozellikler WHERE model IN (SELECT model FROM Ozellikler GROUP BY model HAVING COUNT(distinct ProductID) > 1) order by model")
    rows = cur.fetchall()

    kur = con.cursor()
    kur.execute(
        "SELECT distinct model FROM Ozellikler WHERE model IN (SELECT model FROM Ozellikler GROUP BY model HAVING COUNT(distinct ProductID) > 1) order by model")
    kows = kur.fetchall()

    return render_template("duplicate.html", rows=rows, kows=kows)


if __name__ == '__main__':
    # conn = sqlite3.connect("student.db")
    # c = conn.cursor()
    # trendyol_Scrap()
    # vatan_Scrap()
    # hepsiburada_Scrap()
    # n11_scrap()
    # duplicate_Control()
    app.run(debug=True)
