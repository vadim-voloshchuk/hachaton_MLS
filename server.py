from flask import Flask, request
import json
import pandas as pd

app = Flask(__name__)


@app.route("/upload", methods=["POST"]) #['1_Kompanii.xlsx', '2_Produkty_new.xlsx','3_Otrasli.xlsx','4_Tekhnologii.xlsx']
def upload():
    uploaded_files = request.file.getlist("file[]")
    company = pd.read_excel(uploaded_files[0])
    products = pd.read_excel(uploaded_files[1])
    otrosli = pd.read_excel(uploaded_files[2])
    technologi = pd.read_excel(uploaded_files[3])

    otrosliAndTechnologi = otrosli.merge(technologi, on='Создаваемые продукты')

    result = company.merge(products, left_on='global_id', right_on='Компания', how='inner')
    result = result.merge(otrosliAndTechnologi, left_on='product_id', right_on='Создаваемые продукты')

    result = result[
        (result.otrosli_x == result.otrosli_y) &
        (result.podotrosli_x == result.podotrosli_y) &
        (result.technologi3Lvl_x == result.technologi3Lvl_y) &
        (result.technologi2Lvl_x == result.technologi2Lvl_y) &
        (result.technologi1Lvl_x == result.technologi1Lvl_y)]
    result.dropna()
    return result.to_csv('raw.csv')


@app.route("/processing", methods=["POST"])
def processing():
    sector = request.args.get('sector')
    subSector = request.args.get('subSector')
    technologies1Lvl = request.args.get('technologies1Lvl')
    technologies2Lvl = request.args.get('technologies2Lvl')
    technologies3Lvl = request.args.get('technologies3Lvl')
    okpd2 = request.args.get('okpd2')
    description = request.args.get('description')

    return json.dumps({'sector': {'value' : sector, 'check' : True, 'percents': 80 }, 
                        'subSector': {'value' : subSector, 'check' : False, 'percents': 35 },
                        'technologies1Lvl': {'value' : technologies1Lvl, 'check' : True, 'percents': 80 },
                        'technologies2Lvl': {'value' : technologies2Lvl, 'check' : True, 'percents': 80 },
                        'technologies3Lv3': {'value' : technologies3Lv3, 'check' : True, 'percents': 80 },
                        'okpd2': {'value' : okpd2, 'check' : True, 'percents': 80 },
                        'description': {'value' : description,
                        'check' : True, 'percents': 80 }})


if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
