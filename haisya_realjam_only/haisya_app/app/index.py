from flask import Blueprint
from flask import render_template, request, redirect, url_for, session
from .models import Driver, Passenger, Log_History, History 
from . import db
from datetime import datetime
from flask_login import login_required
import random

index = Blueprint("index", __name__)

@index.route("/")
@login_required
def toppage():
    return render_template("toppage.html")

@index.route("/history")
@login_required
def history():
    return render_template("history.html")

@index.route("/criteria", methods=["GET", "POST"])
@login_required
def criteria():
    criteria_count = 1
    return render_template("criteria.html", criteria_count=criteria_count)

@index.route("/criteria_post", methods=["POST"])
@login_required
def criteria_post():
    criteria_count = int(request.form.get("criteria_count"))
    driver_count = 1
    
    select_name = []
    for i in range(criteria_count):
        name = request.form.get(f'criteria[{i}][name]')
        select_name.append(name)

    session["select_name"] = select_name
        
    return render_template("register_d_new.html", driver_count=driver_count, select_name=select_name)

@index.route("/register_d", methods=["GET", "POST"])
@login_required
def register_d():
    driver_count = 1
    return render_template("register_d.html", driver_count=driver_count)

@index.route("/register_d_post", methods=["POST"])
@login_required
def register_d_post():
    if Driver.query.first():
        db.session.query(Driver).delete()
        db.session.commit()

    driver_count = int(request.form.get("driver_count"))

    for i in range(driver_count):
        name = request.form.get(f'driver[{i}][name]')
        old = request.form.get(f'driver[{i}][old]')
        jenre = request.form.get(f'driver[{i}][jenre]')
        capacity = request.form.get(f'driver[{i}][capacity]')
        
        if name is None:
            continue

        new_driver = Driver(name=name, old=old, jenre=jenre, capacity=capacity)
        db.session.add(new_driver)

    db.session.commit()

    return redirect(url_for("index.register_p"))

@index.route("/register_d_post_new", methods=["POST"])
@login_required
def register_d_post_new():
    if Driver.query.first():
        db.session.query(Driver).delete()
        db.session.commit()

    driver_count = int(request.form.get("driver_count"))

    for i in range(driver_count):
        name = request.form.get(f'driver[{i}][name]')
        old = request.form.get(f'driver[{i}][old]')
        jenre = request.form.get(f'driver[{i}][jenre]')
        capacity = request.form.get(f'driver[{i}][capacity]')
        
        if name is None:
            continue

        new_driver = Driver(name=name, old=old, jenre=jenre, capacity=capacity)
        db.session.add(new_driver)

    db.session.commit()

    return redirect(url_for("index.register_p_new"))

@index.route("/register_p", methods=["GET", "POST"])
@login_required
def register_p():
    passenger_count = 1
    return render_template("register_p.html", passenger_count=passenger_count)

@index.route("/register_p_new", methods=["GET", "POST"])
@login_required
def register_p_new():
    passenger_count = 1

    select_name = session.get("select_name")

    return render_template("register_p_new.html", passenger_count=passenger_count, select_name=select_name)


@index.route("/register_p_post",  methods=["POST"])
@login_required
def register_p_post():
    if Passenger.query.first():
        db.session.query(Passenger).delete()
        db.session.commit()

    passenger_count  = int(request.form.get("passenger_count"))

    for i in range(passenger_count):
        name = request.form.get(f'passenger[{i}][name]')
        old = request.form.get(f'passenger[{i}][old]')
        jenre = request.form.get(f'passenger[{i}][jenre]')
        
        if name is None:
            continue    

        new_passenger = Passenger(name=name, old=old, jenre=jenre)
        db.session.add(new_passenger)

    db.session.commit()

    return redirect(url_for("index.match"))

@index.route("/register_p_post_new",  methods=["POST"])
@login_required
def register_p_post_new():
    if Passenger.query.first():
        db.session.query(Passenger).delete()
        db.session.commit()

    passenger_count  = int(request.form.get("passenger_count"))

    for i in range(passenger_count):
        name = request.form.get(f'passenger[{i}][name]')
        old = request.form.get(f'passenger[{i}][old]')
        jenre = request.form.get(f'passenger[{i}][jenre]')
        
        if name is None:
            continue    

        new_passenger = Passenger(name=name, old=old, jenre=jenre)
        db.session.add(new_passenger)

    db.session.commit()

    return redirect(url_for("index.match"))
    
@index.route("/match")
@login_required
def match():
    if Log_History.query.first():
        db.session.query(Log_History).delete()
        db.session.commit()

    driver_list = Driver.query.all()
    passenger_list = Passenger.query.all()
    
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
        remove_length = len(remove)
    
    elif total_capacity == total_passenger:
        remove_length = 0

    # マッチリスト
    matches = {}

    # 残りの乗客を保持しておくリスト
    remain_passengers = passenger_list.copy()

    #　ページを戻った場合のためにcapacityを保存する
    driver_capacity_save = {driver: driver.capacity for driver in driver_list}

    # ジャンルに基づく割り当て
    for driver in driver_list:
        matches[driver] = []
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
            new_match = Log_History(driver_name=driver.name, passenger_name=passenger.name)
            db.session.add(new_match)
    db.session.commit()

    return render_template("result.html", matches=matches, remove_length=remove_length, unassigned_drivers=unassigned_drivers)

@index.route("/save", methods=["GET"])
@login_required
def save():
    error_message = request.args.get("error_message")
    return render_template("naming.html", error_message=error_message)

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
    
    return render_template("history.html", history_names=history_names)

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

    return render_template("history_details.html", drivers=drivers, history_name=history_name)


#　チーム名を自分で決めれる。条件の指定を自分でする。名前で自動入力。