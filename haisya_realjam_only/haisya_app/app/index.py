from flask import Blueprint
from flask import render_template, request, redirect, url_for, session, jsonify
from .models import Group, Team, Driver, CheckedDriver, Passenger, CheckedPassenger, Log_History, History 
from . import db
from datetime import datetime
from flask_login import login_required
import random

index = Blueprint("index", __name__)

@index.route("/")
@login_required
def toppage():
    return render_template("toppage.html")

@index.route("/group_list", methods=["POST"])
@login_required
def group_list():
    groups = Group.query.all()
    return render_template("group_list.html", groups=groups)

@index.route("/post_group/<group_name>", methods=["GET"])
@login_required
def post_group(group_name):
    group_select = Group.query.filter_by(name=group_name).first()
    group_name = group_select.name
    session["group_name"] = group_name
    return redirect(url_for("index.add_driver", group_name=group_name))

@index.route("/delete_group/<group_name>", methods=["POST"])
@login_required
def delete_group(group_name):
    # 指定された名前の履歴をデータベースから削除
    delete_name = Group.query.filter_by(group_name=group_name).first()
    if delete_name:
        teams = Team.query.filter_by(group_id=delete_name.id).all()
        for team in teams:
            db.session.delete(team)
        
        db.session.delete(delete_name)
        db.session.commit
    # 削除後に履歴リストページにリダイレクト
    return redirect(url_for("index.group_list"))

@index.route("/add_group", methods=["GET", "POST"])
@login_required
def add_group():
    criteria_count = 1
    return render_template("add_group.html", criteria_count=criteria_count)

@index.route("/add_group_post", methods=["POST"])
@login_required
def add_group_post():
    driver_count = 1
    criteria_count = int(request.form.get("criteria_count"))
    #グループ名の確認
    group_name = request.form['group_name']
    existing_group = Group.query.filter_by(name=group_name).first()

    if not group_name:
        error_message = "グループ名を入力してください"
        return redirect(url_for("index.add_group", error_message=error_message))
    elif existing_group:
        error_message = f"既に{existing_group.name}は使われています。"
        return redirect(url_for("index.add_group", error_message=error_message))
    else:
        new_group = Group(name=group_name)
        db.session.add(new_group)
        db.session.commit()
    
        for i in range(criteria_count):
            name = request.form.get(f'criteria[{i}][name]')
            new_team = Team(team_name=name, group_id=new_group.id)
            db.session.add(new_team)
        db.session.commit()

    driver_old = {}
    drivers = Driver.query.filter_by(group_name=group_name).all()
    for driver in drivers:
        if driver.old not in driver_old:
            driver_old[driver.old] = []
        driver_old[driver.old].append(driver)
    
    group_select = Group.query.filter_by(name=group_name).first()
    if group_select:
        teams = Team.query.filter_by(group_id=group_select.id).all()
        select_name = [team.team_name for team in teams]

    session["group_name"] = group_name
        
    return render_template("select_d.html", driver_count=driver_count, group_name=group_name, select_name=select_name, drivers=driver_old)

@index.route("/add_driver/<group_name>", methods=["GET", "POST"])
@login_required
def add_driver(group_name):
    group_select = group_select = Group.query.filter_by(name=group_name).first()    
    if group_select:
        teams = Team.query.filter_by(group_id=group_select.id).all()
        select_name = [team.team_name for team in teams]
    
    if request.method == "POST":
        name = request.form['driver_name']
        old = request.form['driver_old']
        jenre = request.form['driver_jenre']
        capacity = request.form['driver_capacity']
        
        new_driver = Driver(group_name=group_name, name=name, old=old, jenre=jenre, capacity=capacity)
        db.session.add(new_driver)
        db.session.commit()
    
    driver_old = {}
    drivers = Driver.query.filter_by(group_name=group_name).all()
    for driver in drivers:
        if driver.old not in driver_old:
            driver_old[driver.old] = []
        driver_old[driver.old].append(driver)

    return render_template("select_d.html", select_name=select_name, drivers=driver_old, group_name=group_name)

@index.route("/delete_driver/<int:driver_id>", methods=["POST"])
@login_required
def delete_driver(driver_id):
    driver = Driver.query.get(driver_id)
    if driver:
        db.session.delete(driver)
        db.session.commit()

    group_name = session.get("group_name")

    group_select = group_select = Group.query.filter_by(name=group_name).first()    
    if group_select:
        teams = Team.query.filter_by(group_id=group_select.id).all()
        select_name = [team.team_name for team in teams]
    
    driver_old = {}
    drivers = Driver.query.filter_by(group_name=group_name).all()
    for driver in drivers:
        if driver.old not in driver_old:
            driver_old[driver.old] = []
        driver_old[driver.old].append(driver)

    return render_template("select_d.html", select_name=select_name, drivers=driver_old, group_name=group_name)


@index.route("/checked_driver", methods=["POST"])
@login_required
def checked_driver():
    group_name = session.get("group_name")
    checked_drivers = request.form.getlist("drivers")
    
    for driver_name in checked_drivers:
        driver = Driver.query.filter_by(name=group_name).filter_by(name=driver_name).first()
        
        checked_driver = CheckedDriver(group_name=driver.group_name, name=driver.name, old=driver.old, jenre=driver.jenre, capacity=driver.capacity)
           
        db.session.add(checked_driver)
        db.session.commit()

    return redirect(url_for("index.add_passenger", group_name=group_name))

@index.route("/add_passenger/<group_name>", methods=["GET", "POST"])
@login_required
def add_passenger(group_name): 
    group_select = Group.query.filter_by(name=group_name).first()
    if group_select:
        teams = Team.query.filter_by(group_id=group_select.id).all()
        select_name = [team.team_name for team in teams]

    if request.method == "POST":
        name = request.form['passenger_name']
        old = request.form['passenger_old']
        jenre = request.form['passenger_jenre']
        
        new_passenger = Passenger(group_name=group_name, name=name, old=old, jenre=jenre)
        db.session.add(new_passenger)
        db.session.commit()
    
    passenger_old = {}
    passengers = Passenger.query.filter_by(group_name=group_name).all()
    for passenger in passengers:
        if passenger.old not in passenger_old:
            passenger_old[passenger.old] = []
        passenger_old[passenger.old].append(passenger)

    return render_template("select_p.html", select_name=select_name, passengers=passenger_old, group_name=group_name)

@index.route("/delete_passenger/<int:passenger_id>", methods=["POST"])
@login_required
def delete_passenger(passenger_id):
    passenger = Passenger.query.get(passenger_id)
    if passenger:
        db.session.delete(passenger)
        db.session.commit()

    group_name = session.get("group_name")

    group_select = group_select = Group.query.filter_by(group_name=group_name).first()    
    if group_select:
        teams = Team.query.filter_by(group_id=group_select.id).all()
        select_name = [team.team_name for team in teams]
    
    passenger_old = {}
    passengers = Passenger.query.filter_by(group_name=group_name).all()
    for passenger in passengers:
        if passenger.old not in passenger_old:
            passenger_old[passenger.old] = []
        passenger_old[passenger.old].append(passenger)

    return render_template("select_d.html", select_name=select_name, passengers=passenger_old, group_name=group_name)


@index.route("/checked_passenger", methods=["POST"])
@login_required
def checked_passenger():
    group_name = session.get("group_name")
    checked_passengers = request.form.getlist("passengers")
    
    for passenger_name in checked_passengers:
        passenger = Passenger.query.filter_by(group_name=group_name).filter_by(name=passenger_name).first()
        
        checked_passenger = CheckedPassenger(group_name=passenger.group_name, name=passenger.name, old=passenger.old, jenre=passenger.jenre)
           
        db.session.add(checked_passenger)
        db.session.commit()

    return redirect(url_for("index.match"))
    
@index.route("/match")
@login_required
def match():
    group_name = session.get("group_name")

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

    return render_template("result.html", matches=matches, remove_length=remove_length, unassigned_drivers=unassigned_drivers, group_name=group_name)

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



