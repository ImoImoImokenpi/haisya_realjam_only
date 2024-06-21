document.addEventListener("DOMContentLoaded", function() {
    var navbarToggler = document.querySelector(".navbar-toggler");
    var navbarCollapse = document.querySelector(".navbar-collapse");

    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener("click", function() {
            navbarCollapse.classList.toggle("show");
        });
    }
});


function addDriver() {
    let driverCount = parseInt(document.getElementById("driver-count").innerText);

    var driverFields = document.getElementById("driver-fields");
    var driverField = document.createElement("div");
    driverField.classList.add("driver-field");
    driverField.id = "driver-field-" + driverCount;
    driverField.innerHTML = `
    <div class="card mb-1" style="border-radius: 1rem;">
    <div class="card-body">
        <div class="form-group mb-1">
            <label class="form-label ms-1" for="name-${driverCount}">名前</label>
            <input type="text" class="form-control form-control-sm rounded-pill" id="name-${driverCount}" name="driver[${driverCount}][name]" required>
            <div class="invalid-feedback"></div>
        </div>
        <div class="form-group mb-1">
            <label for="old-${driverCount}" class="form-label ms-1">学年</label>
            <select id="old" class="form-control form-control-sm rounded-pill" name="driver[${driverCount}][old]">
                <option value="M1">M1</option>
                <option value="M2">M2</option>
                <option value="B4">B4</option>
                <option value="B3">B3</option>
                <option value="B2">B2</option>
                <option value="B1">B1</option>
            </select>
        </div>
        <div class="form-group mb-1">
            <label for="jenre-${driverCount}" class="form-label ms-1">ジャンル</label>
            <select id="jenre-${driverCount}" class="form-control form-control-sm rounded-pill" name="driver[${driverCount}][jenre]">
                <option value="HIPHOP">HIPHOP</option>
                <option value="LOCK">LOCK</option>
                <option value="POP">POP</option>
                <option value="BREAK">BREAK</option>
                <option value="WAACK">WAACK</option>
                <option value="HOUSE">HOUSE</option>
                <option value="JAZZ">JAZZ</option>
            </select>
        </div>
        <div class="form-group mb-1">
            <label for="capacity-${driverCount}" class="form-label ms-1">定員</label>
            <select id="capacity-${driverCount}" class="form-control form-control-sm rounded-pill" name="driver[${driverCount}][capacity]">
                <option value="8">8</option>
                <option value="7">7</option>
                <option value="6">6</option>
                <option value="5">5</option>
                <option value="4">4</option>
                <option value="3">3</option>
                <option value="2">2</option>
                <option value="1">1</option>
            </select>
        </div>
    </div>
    <button type="button" class="btn btn-danger btn-sm btn-close" aria-label="Close" onclick="removeDriverField(this)"></button>
    </div>
    `;
    driverFields.appendChild(driverField);
    driverCount++;
    document.getElementById("driver-count").innerText = driverCount;
    // ループ回数の増減
    document.getElementById("driver-count-input").value = driverCount;
}

function addPassenger() {
    let passengerCount = parseInt(document.getElementById("passenger-count").innerText);
    
    var passengerFields = document.getElementById("passenger-fields");
    var passengerField = document.createElement("div");
    passengerField.classList.add("passenger-field");
    passengerField.id = "passenger-field-" + passengerCount;
    passengerField.innerHTML = `
    <div class="card mb-1" style="border-radius: 1rem;">
    <div class="card-body">
        <div class="form-group mb-1">
            <label class="form-label ms-1" for="name-${passengerCount}">名前</label>
            <input type="text" class="form-control form-control-sm rounded-pill" id="name-${passengerCount}" name="passenger[${passengerCount}][name]" required>
            <div class="invalid-feedback"></div>
        </div>
        <div class="form-group mb-1">
            <label for="old-${passengerCount}" class="form-label ms-1">学年</label>
            <select id="old" class="form-control form-control-sm rounded-pill" name="passenger[${passengerCount}][old]">
                <option value="M1">M1</option>
                <option value="M2">M2</option>
                <option value="B4">B4</option>
                <option value="B3">B3</option>
                <option value="B2">B2</option>
                <option value="B1">B1</option>
            </select>
        </div>
        <div class="form-group mb-1">
            <label for="jenre-${passengerCount}" class="form-label ms-1">ジャンル</label>
            <select id="jenre-${passengerCount}" class="form-control form-control-sm rounded-pill" name="passenger[${passengerCount}][jenre]">
                <option value="HIPHOP">HIPHOP</option>
                <option value="LOCK">LOCK</option>
                <option value="POP">POP</option>
                <option value="BREAK">BREAK</option>
                <option value="WAACK">WAACK</option>
                <option value="HOUSE">HOUSE</option>
                <option value="JAZZ">JAZZ</option>
            </select>
        </div>
    </div>
    <button type="button" class="btn btn-danger btn-sm btn-close" aria-label="Close" onclick="removePassengerField(this)"></button>
    </div>
    `;
    passengerFields.appendChild(passengerField);
    passengerCount++;
    document.getElementById("passenger-count").innerText = passengerCount;
    // ループ回数の増減
    document.getElementById("passenger-count-input").value = passengerCount;
}

function addDriverNew() {
    let driverCount = parseInt(document.getElementById("driver-count").innerText);

    var driverFields = document.getElementById("driver-fields");
    var driverField = document.createElement("div");
    driverField.classList.add("driver-field");
    driverField.id = "driver-field-" + driverCount;
    driverField.innerHTML = `
    <div class="card mb-1" style="border-radius: 1rem;">
    <div class="card-body">
        <div class="form-group mb-1">
            <label class="form-label ms-1" for="name-${driverCount}">名前</label>
            <input type="text" class="form-control form-control-sm rounded-pill" id="name-${driverCount}" name="driver[${driverCount}][name]" required>
            <div class="invalid-feedback"></div>
        </div>
        <div class="form-group mb-1">
            <label for="old-${driverCount}" class="form-label ms-1">学年</label>
            <select id="old" class="form-control form-control-sm rounded-pill" name="driver[${driverCount}][old]">
                <option value="M1">M1</option>
                <option value="M2">M2</option>
                <option value="B4">B4</option>
                <option value="B3">B3</option>
                <option value="B2">B2</option>
                <option value="B1">B1</option>
            </select>
        </div>
        <div class="form-group mb-1">
            <label for="jenre-${driverCount}" class="form-label ms-1">チーム</label>
            <select id="jenre-${driverCount}" class="form-control form-control-sm rounded-pill" name="driver[${driverCount}][jenre]">
            ${selectName.map(team => `<option value="${team}">${team}</option>`).join('')}
            </select>
        </div>
        <div class="form-group mb-1">
            <label for="capacity-${driverCount}" class="form-label ms-1">定員</label>
            <select id="capacity-${driverCount}" class="form-control form-control-sm rounded-pill" name="driver[${driverCount}][capacity]">
                <option value="8">8</option>
                <option value="7">7</option>
                <option value="6">6</option>
                <option value="5">5</option>
                <option value="4">4</option>
                <option value="3">3</option>
                <option value="2">2</option>
                <option value="1">1</option>
            </select>
        </div>
    </div>
    <button type="button" class="btn btn-danger btn-sm btn-close" aria-label="Close" onclick="removeDriverField(this)"></button>
    </div>
    `;
    driverFields.appendChild(driverField);
    driverCount++;
    document.getElementById("driver-count").innerText = driverCount;
    // ループ回数の増減
    document.getElementById("driver-count-input").value = driverCount;
}

function addPassengerNew() {
    let passengerCount = parseInt(document.getElementById("passenger-count").innerText);
    
    var passengerFields = document.getElementById("passenger-fields");
    var passengerField = document.createElement("div");
    passengerField.classList.add("passenger-field");
    passengerField.id = "passenger-field-" + passengerCount;
    passengerField.innerHTML = `
    <div class="card mb-1" style="border-radius: 1rem;">
    <div class="card-body">
        <div class="form-group mb-1">
            <label class="form-label ms-1" for="name-${passengerCount}">名前</label>
            <input type="text" class="form-control form-control-sm rounded-pill" id="name-${passengerCount}" name="passenger[${passengerCount}][name]" required>
            <div class="invalid-feedback"></div>
        </div>
        <div class="form-group mb-1">
            <label for="old-${passengerCount}" class="form-label ms-1">学年</label>
            <select id="old" class="form-control form-control-sm rounded-pill" name="passenger[${passengerCount}][old]">
                <option value="M1">M1</option>
                <option value="M2">M2</option>
                <option value="B4">B4</option>
                <option value="B3">B3</option>
                <option value="B2">B2</option>
                <option value="B1">B1</option>
            </select>
        </div>
        <div class="form-group mb-1">
            <label for="jenre-${passengerCount}" class="form-label ms-1">チーム</label>
            <select id="jenre-${passengerCount}" class="form-control form-control-sm rounded-pill" name="passenger[${passengerCount}][jenre]">
            ${selectName.map(team => `<option value="${team}">${team}</option>`).join('')}
            </select>
        </div>
    </div>
    <button type="button" class="btn btn-danger btn-sm btn-close" aria-label="Close" onclick="removePassengerField(this)"></button>
    </div>
    `;
    passengerFields.appendChild(passengerField);
    passengerCount++;
    document.getElementById("passenger-count").innerText = passengerCount;
    // ループ回数の増減
    document.getElementById("passenger-count-input").value = passengerCount;
}

function addCriteria() {
    let criteriaCount = parseInt(document.getElementById("criteria-count").innerText);
    
    var criteriaFields = document.getElementById("criteria-fields");
    var criteriaField = document.createElement("div");
    criteriaField.classList.add("criteria-field");
    criteriaField.id = "criteria-field-" + criteriaCount;
    criteriaField.innerHTML = `
    <div class="card mb-1" style="border-radius: 1rem;">
    <div class="card-body">
        <div class="form-group mb-1">
            <label class="form-label ms-1" for="name-${criteriaCount}">チーム名</label>
            <input type="text" class="form-control form-control-sm rounded-pill" id="name-${criteriaCount}" name="criteria[${criteriaCount}][name]" required>
            <div class="invalid-feedback"></div>
        </div>                                
    </div>
    <button type="button" class="btn btn-danger btn-sm btn-close" aria-label="Close" onclick="removeCriteriaField(this)"></button>
    </div>
    `;
    criteriaFields.appendChild(criteriaField);
    criteriaCount++;
    document.getElementById("criteria-count").innerText = criteriaCount;
    // ループ回数の増減
    document.getElementById("criteria-count-input").value = criteriaCount;
}

function removeDriverField(button) {
    var driverField = button.parentNode.parentNode;
    var driverFields = driverField.parentNode;
    driverFields.removeChild(driverField);

    // 削除されたフィールドのインデックスを取得
    var fields = driverFields.getElementsByClassName("driver-field");
    for (var i = 0; i < fields.length; i++) {
        var newIndex = i;
        var currentId = fields[i].id.split("-");
        fields[i].id = currentId[0] + "-" + currentId[1] + "-" + newIndex;
        fields[i].querySelector("label[for^='name-']").setAttribute("for", "name-" + newIndex);
        fields[i].querySelector("input[name^='driver']").setAttribute("name", "driver[" + newIndex + "][name]");
        fields[i].querySelector("label[for^='old-']").setAttribute("for", "old-" + newIndex);
        fields[i].querySelector("select[name^='driver'][name$='[old]']").setAttribute("name", "driver[" + newIndex + "][old]");
        fields[i].querySelector("label[for^='jenre-']").setAttribute("for", "jenre-" + newIndex);
        fields[i].querySelector("select[name^='driver'][name$='[jenre]']").setAttribute("name", "driver[" + newIndex + "][jenre]");
        fields[i].querySelector("label[for^='capacity-']").setAttribute("for", "capacity-" + newIndex);
        fields[i].querySelector("select[name^='driver'][name$='[capacity]']").setAttribute("name", "driver[" + newIndex + "][capacity]");
        fields[i].querySelector("button").setAttribute("onclick", "removeDriverField(this)");
    }

    let driverCount = fields.length;
    document.getElementById("driver-count").innerText = driverCount;
    document.getElementById("driver-count-input").value = driverCount;
}


function removePassengerField(button) {
    var passengerField = button.parentNode.parentNode;
    var passengerFields = passengerField.parentNode;
    passengerFields.removeChild(passengerField);

    // 削除されたフィールドのインデックスを取得
    var fields = passengerFields.getElementsByClassName("passenger-field");
    for (var i = 0; i < fields.length; i++) {
        var newIndex = i;
        var currentId = fields[i].id.split("-");
        fields[i].id = currentId[0] + "-" + currentId[1] + "-" + newIndex;
        fields[i].querySelector("label[for^='name-']").setAttribute("for", "name-" + newIndex);
        fields[i].querySelector("input[name^='passenger']").setAttribute("name", "passenger[" + newIndex + "][name]");
        fields[i].querySelector("label[for^='old-']").setAttribute("for", "old-" + newIndex);
        fields[i].querySelector("select[name^='passenger'][name$='[old]']").setAttribute("name", "passenger[" + newIndex + "][old]");
        fields[i].querySelector("label[for^='jenre-']").setAttribute("for", "jenre-" + newIndex);
        fields[i].querySelector("select[name^='passenger'][name$='[jenre]']").setAttribute("name", "passenger[" + newIndex + "][jenre]");
        fields[i].querySelector("button").setAttribute("onclick", "removePassengerField(this)");
    }

    let passengerCount = fields.length;
    document.getElementById("passenger-count").innerText = passengerCount;
    document.getElementById("passenger-count-input").value = passengerCount;
}

function removeCriteriaField(button) {
    var criteriaField = button.parentNode.parentNode;
    var criteriaFields = criteriaField.parentNode;
    criteriaFields.removeChild(criteriaField);

    // 削除されたフィールドのインデックスを取得
    var fields = criteriaFields.getElementsByClassName("criteria-field");
    for (var i = 0; i < fields.length; i++) {
        var newIndex = i;
        var currentId = fields[i].id.split("-");
        fields[i].id = currentId[0] + "-" + currentId[1] + "-" + newIndex;
        fields[i].querySelector("label[for^='name-']").setAttribute("for", "name-" + newIndex);
        fields[i].querySelector("input[name^='criteria']").setAttribute("name", "criteria[" + newIndex + "][name]");
        fields[i].querySelector("button").setAttribute("onclick", "removeCriteriaField(this)");
    }

    let criteriaCount = fields.length;
    document.getElementById("criteria-count").innerText = criteriaCount;
    document.getElementById("criteria-count-input").value = criteriaCount;
}

function checkForm() {
    // fieldのチェック
    var driverFields = document.getElementsByClassName("driver-field");
    for (var i = 0; i < driverFields.length; i++) {
        var name = driverFields[i].querySelector("input[name^='driver'][name$='[name]']").value;
        if (name.trim() === "") {
            alert("Please fill in all driver fields.");
            // driverfieldがi回終われば、送信される
            return false;
        }
    }

    // fieldのチェック
    var passengerFields = document.getElementsByClassName("passenger-field");
    for (var i = 0; i < passengerFields.length; i++) {
        var name = passengerFields[i].querySelector("input[name^='passenger'][name$='[name]']").value;
        if (name.trim() === "") {
            alert("Please fill in all passenger fields.");
            // driverfieldがi回終われば、送信される
            return false;
        }
    }

    // フォーム送信
    return true;
}

function checkNaming() {
    // fieldのチェック
    var namingField = document.querySelector("input[name='history[name]']");
    var naming = namingField.value.trim();
    if (naming === "") {
        alert("履歴名を入力してください。");
        return false;
    }
    return true;
}

document.addEventListener('DOMContentLoaded', function() {
    var deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var historyName = this.dataset.name;
            if (confirm('この履歴を削除しますか？')) {
                deleteHistory(historyName);
            }
        });
    });

    function deleteHistory(historyName) {
        fetch('/delete_history/' + historyName, {
            method: 'POST',
        })
        .then(function(response) {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            // 削除が成功したら、履歴リストを再読込する
            reloadHistoryList();
        })
        .catch(function(error) {
            console.error('There was a problem with the fetch operation:', error);
        });
    }

    function reloadHistoryList() {
        // 履歴リストを再読込するために、履歴リストページにリダイレクトする
        window.location.href = '/history_list';
    }
});

window.onload = function() {
    changeColor('textimage');
    changeColor('clipimage');
};

function changeColor(imageId) {
    // 画像要素を取得
    var image = document.getElementById(imageId);
    
        // 画像内のピクセルデータにアクセス
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    canvas.width = image.width;
    canvas.height = image.height;
    context.drawImage(image, 0, 0);
    var imageData = context.getImageData(0, 0, image.width, image.height);
    var data = imageData.data;

        // 画像内の特定の色を変更する
    for (var i = 0; i < data.length; i += 4) {
        // 赤、緑、青の値を取得
        data[i] = 255;    // Red
        data[i + 1] = 255; // Green
        data[i + 2] = 255; // Blue
    }

    context.putImageData(imageData, 0, 0);

    image.src = canvas.toDataURL();
}

function copyText() {
    // コピーするテキストを取得
    var resultArea = document.getElementById("resultArea")
    
    var textToCopy = "";

    var drivers = resultArea.querySelectorAll('.card-title');
    drivers.forEach(function(driverElement) {
        // ドライバー名を取得
        var driverName = driverElement.innerText;
        // 乗客リストを取得
        var passengerList = driverElement.nextElementSibling.getElementsByTagName("li");
        var passengersText = "";
        for (var i = 0; i < passengerList.length; i++) {
            passengersText += passengerList[i].innerText + "\n";
        }
        // ドライバー名と乗客リストを結合
        textToCopy += driverName + ":\n" + passengersText + "\n";
    });

    var tempTextArea = document.createElement("textarea");
    tempTextArea.value = textToCopy;
    tempTextArea.style.position = "fixed"; // 要素が画面外に行かないように
    document.body.appendChild(tempTextArea);
    // テキストエリアを選択し、コピー
    tempTextArea.select();
    document.execCommand("copy");
    // 不要なテキストエリアを削除
    document.body.removeChild(tempTextArea);
    // ユーザーにコピーされた旨を通知する（任意）
    alert("配車結果がクリップボードにコピーされました。");
}

function copyUrl() {
    var currentURL = window.location.href; // 現在のURLを取得
    navigator.clipboard.writeText(currentURL); // URLをクリップボードにコピー
    alert("クリップボードにURLがコピーされました: " + currentURL); // コピーされたことを通知
}