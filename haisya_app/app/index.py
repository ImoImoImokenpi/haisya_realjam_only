from flask import Blueprint
from flask import render_template, request, redirect, url_for, session, jsonify
from .models import Driver, CheckedDriver, Passenger, CheckedPassenger, Log_History, History 
from . import db
from datetime import datetime
from flask_login import login_required
import random

index = Blueprint("index", __name__)

@index.route("/")
@login_required
def toppage():
    return render_template("toppage.html")

@index.route("/add_driver", methods=["GET", "POST"])
@login_required
def add_driver():
    if CheckedDriver.query.first():
        db.session.query(CheckedDriver).delete()
        db.session.commit()

    if request.method == "POST":
        name = request.form['driver_name']
        old = request.form['driver_old']
        jenre = request.form['driver_jenre']
        capacity = request.form['driver_capacity']
        
        new_driver = Driver(name=name, old=old, jenre=jenre, capacity=capacity)
        db.session.add(new_driver)
        db.session.commit()

        return redirect(url_for("index.add_driver"))
    
    all_drivers = Driver.query.all()
    driver_by_old = {}
    for driver in all_drivers:
        if driver.old not in driver_by_old:
            driver_by_old[driver.old] = []
        driver_by_old[driver.old].append(driver)

    return render_template("driver/select_d.html", drivers=driver_by_old)

@index.route("/delete_driver/<int:driver_id>", methods=["POST"])
@login_required
def delete_driver(driver_id):
    driver = Driver.query.get(driver_id)
    if driver:
        db.session.delete(driver)
        db.session.commit()

    all_drivers = Driver.query.all()
    driver_by_old = {}
    for driver in all_drivers:
        if driver.old not in driver_by_old:
            driver_by_old[driver.old] = []
        driver_by_old[driver.old].append(driver)

    return render_template("driver/select_d.html", drivers=driver_by_old)

@index.route("/checked_driver", methods=["POST"])
@login_required
def checked_driver():
    checked_drivers_ids = request.form.getlist("drivers")
    for  driver_id_str in checked_drivers_ids:
        driver_id = int(driver_id_str)
        section = request.form.get(f'section-{driver_id}')
    
        driver = Driver.query.get(driver_id)
        if driver and section:
            checked_driver = CheckedDriver(
                name=driver.name, 
                old=driver.old,
                jenre=driver.jenre,
                section=section, 
                capacity=driver.capacity
            )
            db.session.add(checked_driver)

    db.session.commit()
    return redirect(url_for("index.add_passenger"))

@index.route("/add_passenger", methods=["GET", "POST"])
@login_required
def add_passenger(): 
    if CheckedPassenger.query.first():
        db.session.query(CheckedPassenger).delete()
        db.session.commit()

    if request.method == "POST":
        name = request.form['passenger_name']
        old = request.form['passenger_old']
        jenre = request.form['passenger_jenre']
        
        new_passenger = Passenger(name=name, old=old, jenre=jenre)
        db.session.add(new_passenger)
        db.session.commit()

        return redirect(url_for("index.add_passenger"))
    
    passenger_by_old = {}
    all_passengers = Passenger.query.all()
    for passenger in all_passengers:
        if passenger.old not in passenger_by_old:
            passenger_by_old[passenger.old] = []
        passenger_by_old[passenger.old].append(passenger)

    return render_template("passenger/select_p.html", passengers=passenger_by_old)

@index.route("/delete_passenger/<int:passenger_id>", methods=["POST"])
@login_required
def delete_passenger(passenger_id):
    passenger = Passenger.query.get(passenger_id)
    if passenger:
        db.session.delete(passenger)
        db.session.commit()

    passenger_by_old = {}
    all_passengers = Passenger.query.all()
    for passenger in all_passengers:
        if passenger.old not in passenger_by_old:
            passenger_by_old[passenger.old] = []
        passenger_by_old[passenger.old].append(passenger)

    return render_template("passenger/select_p.html", passengers=passenger_by_old)


@index.route("/checked_passenger", methods=["POST"])
@login_required
def checked_passenger():
    checked_passengers_ids = request.form.getlist("passengers")
    for passenger_id_str in checked_passengers_ids:
        passenger_id = int(passenger_id_str)
        section = request.form.get(f'section-{passenger_id}')
    
        passenger = Passenger.query.get(passenger_id)
        if passenger and section:
            checked_passenger = CheckedPassenger(
                name=passenger.name, 
                old=passenger.old,
                jenre=passenger.jenre,
                section=section, 
            )
            db.session.add(checked_passenger)

    db.session.commit()
    return redirect(url_for("index.match"))
    
@index.route("/log")
@login_required
def log():
    driver_list = CheckedDriver.query.all()
    passenger_list = CheckedPassenger.query.all()

    return render_template("log/log.html", drivers=driver_list, passengers=passenger_list)

@index.route("/match")
@login_required
def match():
    if Log_History.query.first():
        db.session.query(Log_History).delete()
        db.session.commit()

    driver_list = CheckedDriver.query.all()
    passenger_list = CheckedPassenger.query.all()
    
    # リストの順番をシャッフルし、偏りを減らす
    random.shuffle(driver_list)
    random.shuffle(passenger_list)

    # 乗客のあまりを抜いておく
    total_capacity = sum(driver.capacity for driver in driver_list)
    total_passenger = len(passenger_list)
    
    remove_length = 0

    if total_capacity <= total_passenger:
        difference = total_passenger - total_capacity
        remove = random.sample(passenger_list, difference)
        remove_length = difference
    
    elif total_capacity == total_passenger:
        remove_length = 0

    # マッチリスト
    matches = {}

    # 残りの乗客を保持しておくリスト(乗客リストのコピーから取り除いていく)
    remain_passengers = passenger_list.copy()

    #　ページを戻った場合のためにcapacityを保存する
    driver_capacity_save = {driver: driver.capacity for driver in driver_list}
    
    # セクションとジャンルで割り当て
    for driver in driver_list:
        matches[driver] = []
        section_matches = []
        if driver.capacity > 0:
            for passenger in remain_passengers:
                if passenger.section == driver.section and passenger.jenre == driver.jenre:
                    if driver.capacity > 0:
                        section_matches.append(passenger)
                        driver.capacity -= 1
            matches[driver].extend(section_matches)
            remain_passengers = [passenger for passenger in remain_passengers if passenger not in matches[driver]]
    
    # セクションで割り当て
    for driver in driver_list:
        section_matches = []
        if driver.capacity > 0:
            for passenger in remain_passengers:
                if passenger.section == driver.section:
                    if driver.capacity > 0:
                        section_matches.append(passenger)
                        driver.capacity -= 1
            matches[driver].extend(section_matches)
            remain_passengers = [passenger for passenger in remain_passengers if passenger not in matches[driver]]

    # ジャンルに基づく割り当て
    for driver in driver_list:
        jenre_matches = []
        if driver.capacity > 0:
            for passenger in remain_passengers:
                if passenger.jenre == driver.jenre:
                    if driver.capacity > 0:
                        jenre_matches.append(passenger)
                        driver.capacity -= 1
            matches[driver].extend(jenre_matches)
            remain_passengers = [passenger for passenger in remain_passengers if passenger not in matches[driver]]

    # 学年に基づく割り当て
    for driver in driver_list:
        old_matches = []
        if driver.capacity > 0:
            for passenger in remain_passengers:
                if passenger.old == driver.old:
                    if driver.capacity > 0:
                        old_matches.append(passenger)
                        driver.capacity -= 1
            matches[driver].extend(old_matches)
            remain_passengers = [passenger for passenger in remain_passengers if passenger not in matches[driver]]

    # 残りの乗客をランダムに割り当て
    for driver in driver_list:
        if driver.capacity > 0:
            random_matches = random.sample(remain_passengers, min(driver.capacity, len(remain_passengers)))
            for passenger in random_matches:
                if driver.capacity > 0:
                    matches[driver].append(passenger)
                    driver.capacity -= 1

    unassigned_drivers = [driver.name for driver in driver_list if not matches[driver]]

    for driver in driver_list:
        driver.capacity = driver_capacity_save[driver]
    

    for driver, passengers in matches.items():
        for passenger in passengers:
            driver_info = f"{driver.name} / {driver.jenre} / {driver.old}"
            passenger_info = f"{passenger.name} / {passenger.jenre} / {passenger.old}"
            new_match = Log_History(driver_name=driver_info, passenger_name=passenger_info)
            db.session.add(new_match)
    db.session.commit()

    return render_template("result/result.html", matches=matches, remove_length=remove_length, unassigned_drivers=unassigned_drivers)

@index.route("/save", methods=["GET"])
@login_required
def save():
    error_message = request.args.get("error_message")
    return render_template("result/naming.html", error_message=error_message)

@index.route("/naming", methods=["POST"])
@login_required
def naming():
    history_name = request.form.get("history[name]")
    existing_name = History.query.filter_by(history_name=history_name).first()

    if not history_name:
        error_message = "配車名を入力してください。"
        return redirect(url_for("index.save", error_message=error_message))
    elif existing_name:
        error_message = f"既に{existing_name.history_name}は使われています。"
        return redirect(url_for("index.save", error_message=error_message))
    else:
        log_matches = Log_History.query.all()
        created_date = datetime.utcnow() 
        for log_match in log_matches:
            new_match = History(driver_name=log_match.driver_name, passenger_name=log_match.passenger_name, history_name=history_name, created_date=created_date)
            db.session.add(new_match)
        
        db.session.query(Log_History).delete()
        db.session.commit()
        return redirect(url_for("index.history_list"))

@index.route("/history_list", methods=["GET", "POST"])
@login_required
def history_list():
    histories = History.query.all()
    sorted_histories = sorted(histories, key=lambda x: x.created_date, reverse=True)

    history_names = []
    seen_names = set()  # 重複を確認するためのセット

    for history in sorted_histories:
        # 履歴名がセットに含まれていなければリストに追加
        if history.history_name not in seen_names:
            history_names.append((history.history_name, history.created_date))
            seen_names.add(history.history_name)
    
    return render_template("history/history.html", history_names=history_names)

@index.route("/delete_history/<history_name>", methods=["POST"])
@login_required
def delete_history(history_name):
    # 指定された名前の履歴をデータベースから削除
    delete_names = History.query.filter_by(history_name=history_name).all()
    for delete_name in delete_names:
        db.session.delete(delete_name)
    db.session.commit()
    
    # 削除後に履歴リストページにリダイレクト
    return redirect(url_for("index.history_list"))

@index.route("/history_list/<history_name>")
@login_required
def history_details(history_name):
    history_details = History.query.filter_by(history_name=history_name).all()
    
    drivers = {}
    for history_detail in history_details:
        driver = history_detail.driver_name
        passenger = history_detail.passenger_name
        if driver not in drivers:
            drivers[driver] = [passenger]
        else:
            drivers[driver].append(passenger)

    return render_template("history/history_details.html", drivers=drivers, history_name=history_name)





