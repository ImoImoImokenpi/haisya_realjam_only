document.addEventListener("DOMContentLoaded", function() {
    var navbarToggler = document.querySelector(".navbar-toggler");
    var navbarCollapse = document.querySelector(".navbar-collapse");

    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener("click", function() {
            navbarCollapse.classList.toggle("show");
        });
    }
});

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