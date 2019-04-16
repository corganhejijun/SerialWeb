
function applyFilter(chartlist){
    var portName = $("#filter-select").val();
    var checked = $("#checkbox-filter")[0].checked;
    for (var i = 0; i < chartlist.length; i++){
        chartlist[i][0].contentWindow.applyFilter(portName, checked);
    }
}

function getDataDown(button, downloadFormat){
    var name = button.value;
    $("#myModalLabel")[0].innerHTML = "串口" + name + "数据";
    var result = downloadFormat(name);
    if (result.length > 0)
        $("#myModalData")[0].innerHTML = result;
    else{
        $("#myModalLabel")[0].innerHTML = "串口" + name + "无数据";
        $("#myModalData")[0].innerHTML = "";
    }
}

function setPortButton(result, serialData){
    var buttonList = $("button.com");
    for (var j = 0; j < buttonList.length; j ++){
        var button = buttonList[j];
        for (var i = 0; i < result.openList.length; i++){
            if (button.value == result.openList[i]){
                $(button).removeClass('btn-success').addClass('btn-danger');
                button.innerHTML = "关闭" + button.value;
            }
        }
    }
    for (var i = 0; i < result.occupy.length; i++){
        $(".top")[0].innerHTML += "<button class='btn btn-default' disabled=true>" + result.occupy[i] + "被占用</button>"
    }
    buttonList.on('click', function(){
        var btn = $(this);
        if (btn.hasClass('btn-success')){
            $.ajax({url: 'http://' + window.location.host + "/json",
                async : false,
                data: {func: "open", name:btn.val(), baud:$('#baudrate').val()},
                success: function(result){
                    if (result.flag == false){
                        alert("打开失败");
                        return;
                    }
                    btn.html("关闭" + btn.val());
                    btn.removeClass('btn-success').addClass('btn-danger');
                    serialData.openPort(btn.val());
                }
            });
        }
        else if (btn.hasClass('btn-danger')){
            $.ajax({url: 'http://' + window.location.host + "/json",
                async : false,
                data: {func:"close", name:btn.val()},
                success: function(result){
                    if (result.flag == false){
                        alert("关闭失败");
                        return;
                    }
                    btn.html("打开" + btn.val());
                    btn.removeClass('btn-danger').addClass('btn-success');
                    serialData.closePort(btn.val());
                }
            });
        }
    });
}

function checkPortList(serialData, downloadFormat){
    $.ajax({url: 'http://' + window.location.host + "/json",
        data: {func: "checkOpen"},
        async : false,
        success: function(result){
            if (result.flag == false)
                return;
            setPortButton(result, serialData);
            $("button.download").on('click', function(){
                getDataDown($(this)[0], downloadFormat);
                $('#myModal').modal();
            });
        }
    });
}

function SerialData(updateChart, getData, dataList){
    this.getMsgTimer = null;
    this.getData = getData;
    this.updateChart = updateChart;
    this.dataList = dataList;
}

SerialData.prototype.openPort = function(portName){
    for (var i = 0; i < this.dataList.length; i++){
        if (this.dataList[i].name == portName){
            // delete the closed port data
            this.dataList[i].opened = true;
            break;
        }
    }
    this.getSerialData();
}

SerialData.prototype.closePort = function(portName){
    var openedList = [];
    for (var i = 0; i < this.dataList.length; i++){
        if (this.dataList[i].name == portName){
            // delete the closed port data
            this.dataList[i].opened = false;
            if (this.dataList[i].opened)
                openedList.push(this.dataList[i].name);
            break;
        }
    }
    if (openedList.length == 0){
        clearInterval(this.getMsgTimer);
        this.getMsgTimer = null;
        return;
    }
}

SerialData.prototype.serialProcess = function(msg){
    var comName = msg.substring(0, msg.indexOf(":"))
    for (var j = 0; j < this.dataList.length; j++){
        if (this.dataList[j].name == comName){
            var allData = msg.substring(msg.indexOf(":") + 1);
            var allDataList = allData.split('\n');
            for (var x = 0; x < allDataList.length; x++){
                this.getData(allDataList[x], j);
                for (var k = 0; k < this.dataList[j].data.length; k++){
                    // 最多存储30分钟数据
                    var data = this.dataList[j].data[k];
                    if (data.length < 100 || data.data.length == 0)
                        continue;
                    var time = data.data[0].value[0];
                    var time2 = data.data[data.data.length - 1].value[0];
                    if (time2.getTime() - time.getTime() > 30 * 60 * 1000){ 
                        data.data.shift();
                    }
                }
            }
            break;
        }
    }
}

SerialData.prototype.getSerialData = function(){
    var openedList = [];
    var dataList = this.dataList;
    var self = this;
    for (var i = 0; i < dataList.length; i++){
        if (dataList[i].opened)
            openedList.push(dataList[i].name);
    }
    if (openedList.length == 0){
        clearInterval(this.getMsgTimer);
        this.getMsgTimer = null;
        return;
    }
    if (this.getMsgTimer != null)
        return;
    this.getMsgTimer = setInterval(function(){
        var opened = [];
        for (var i = 0; i < dataList.length; i++){
            if (dataList[i].opened)
                opened.push(dataList[i].name);
        }
        $.ajax({url: 'http://' + window.location.host + "/json",
            data: {func: "read", name:opened.join(",")},
            async : false,
            success: function(result){
                if (result.flag == false){
                    alert("读取失败");
                    return;
                }
                if (result.msg.length == 0)
                    return;
                for (var i = 0; i < result.msg.length; i++){
                    self.serialProcess(result.msg[i]);
                }
                self.updateChart();
            }
        })
    }, 1000);
}  