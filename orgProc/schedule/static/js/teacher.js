var subjID;
var planID;
var selLessonId;

var loadedLessons;

var ccrf;
// 
function selectSubject(subjectUID, justUpdate=false) {
    subjID = subjectUID;
    // подгрузка через ajax
    sendReq(
        "GET",
        {
            "action": "teachSubj",
            "subjId": subjectUID
        },
        function (data) {
            if (data != "500" && data != "400"){
                console.log(data);
                renderSelSubj(data); 
                // 
                if(!justUpdate)
                {
                    closeSubj();
                    $(".selSubj").removeClass("hiden");
                    scrollTo("descr");
                }
            }
                
                else
                alert("ошибка загрузки информации о занятии, обратитесь к системному администратору");
        });
    
}

function openSubjPlan(alfa=1) {
    // подгрузка через ajax
    sendReq(
        "GET",
        {
            "action": "teachPlan",
            "subjId": subjID,
            "planId": planID
        },
        function (data) {
            console.log(data);
            renderPlan(data,alfa);

            $(".subjPlan").removeClass("hiden");
            scrollTo("plan");
        }

    );
     
}

// ==============
function closePlan() {
    $(".selSubj").addClass("hiden");
    closeSubj();
}
function closeSubj() {
    $(".subjPlan").addClass("hiden");
}

function scrollTo(hash) {
    location.hash = "#" + hash;
}
/////////////////////////////////////////////
function sendReq(type, data, succFinc) {
    $.ajax({
        type:type,
        url:"/api/",
        data: data,
        async: true,
        success: function(data){
            succFinc(data);
        }
    });
}
///////////////////////////////////////////
function renderSelSubj(data) {
    // название
    $("#descr").contents().first().replaceWith(data.subjName);
    // прошло занятий
    $("#subPassed").text("прошло занятий: " + data.statistics.subjPass);
    // всего занятий
    $("#subRemain").text("всего: " + data.statistics.subjAll);
    // id
    planID = data.planId;
    // ближайшее занятие
    if (data.nearLesson != "-")
        {
            nearLess = data.nearLesson[0];
        }
    else {
            nearLess = {"theme":"-","date":"-","time":"","description":"-","type":"-","events":{"HW":[],"AddStuff":[]}};
        }
    $("#nearTheme").contents().first().replaceWith("тема занятия: "+ nearLess.theme);
    $("#nearDate").text(nearLess.date + " " + nearLess.time);
    $("#nearDescr").text(nearLess.description);
    $("#nearType").text('тип: '+nearLess.type);

    events = nearLess.events;

    hwHtml = "домашние задания<br>";
    if (events.HW.length>0)
        events.HW.forEach(row => {
            hwHtml+='<a href="'+ row.dls +'" target="_blank"><button>'+ row.name +'</button></a><br>'+ row.description +'<br>';
        });
    else 
        hwHtml +="-";
    $("#nearHw").html(hwHtml);

    stufHtml = "материаллы к занятию<br>";
    if (events.AddStuff.length>0)
        events.AddStuff.forEach(row => {
            stufHtml+='<a href="'+ row.dls +'"target="_blank"><button>'+ row.name +'</button></a><br>'+ row.description +'<br>';
        });
    else 
    stufHtml +="-";
    $("#nearStuff").html(stufHtml);

    // следующее занятие
    if (data.nextLesson != "-")
        {
            nextLess = data.nextLesson[0]
        }
    else {
        nextLess = {"theme":"-","date":"-","time":"","description":"-","type":"-","events":{"HW":[],"AddStuff":[]}};
        }
    $("#nextTheme").contents().first().replaceWith("тема занятия: "+ nextLess.theme);
    $("#nextDate").text(nextLess.date + " " + nextLess.time);
    $("#nextDescr").text(nextLess.description);
    $("#nextType").text('тип: '+nextLess.type);

    events = nextLess.events;

    hwHtml = "домашние задания<br>";
    if (events.HW.length>0)
        events.HW.forEach(row => {
            hwHtml+='<a href="'+ row.dls +'" target="_blank"><button>'+ row.name +'</button></a><br>'+ row.description +'<br>';
        });
    else 
        hwHtml +="-";
    $("#nextHw").html(hwHtml);

    stufHtml = "материаллы к занятию<br>";
    if (events.AddStuff.length>0)
        events.AddStuff.forEach(row => {
            
            stufHtml+='<a href="'+ row.dls +'" target="_blank"><button>'+ row.name +'</button></a><br>'+ row.description +'<br>';
        });
    else 
    stufHtml +="-";
    $("#nextStuff").html(stufHtml);
}

function renderPlan(data,alfa) {
    loadedLessons = data.lessons;
    $("#planTitle").contents().first().replaceWith("план обучения: "+data.subjName);

    blockHtml = "";

    for(num in loadedLessons){
        theme = loadedLessons[num].theme;
        blockHtml+= '<div class="subjItem" num="'+ num +'"> занятие '+ num +' <div class="bold">'+ theme +'</div> </div>';
        
    }
    $(".planLeftCol").html(blockHtml);
    openLesson(alfa);

}
///////
function renderHomework(hwMass) {
    retHtml = '';
    hwMass.forEach(row => {
        retHtml+= '<div><a href="'+ row.dls +'" target="_blank"><button>'+row.name+'</button></a><br>'+row.description+'<button class="close" onclick="delHw('+row.id+')">-</button></div>'
    });
    $(".hvStorage").html(retHtml);

}
function renderStuff(stuffMass) {
    retHtml = '';
    stuffMass.forEach(row => {
        retHtml+= '<div><a href="'+ row.dls +'" target="_blank"><button>'+row.name+'</button></a><br>'+row.description+'<button class="close" onclick="delStuff('+row.id+')">-</button></div>'
    });
    $(".stuffStorage").html(retHtml);
}

/////////////////////// 
$(document).ready ( function () {
    $(".planLeftCol").on ("click", ".subjItem", function () {
        openLesson($(this).attr("num"));
    });

    $("#inpName").focusout(function(){
        saveLesson();
    });
    $("#inpDescr").focusout(function(){
        saveLesson();
    });
});
// 
function openLesson(num){
    selLessonId = num;
    $(".selectedItem").removeClass("selectedItem");
    $(".subjItem").eq(num-1).addClass("selectedItem");
    // 
    $(".planRightCol").contents().first().replaceWith("занятие " + num + " от " + loadedLessons[num].date + " " + loadedLessons[num].time);
    // 
    $("#inpName").val(loadedLessons[num].theme);
    $("#inpDescr").val(loadedLessons[num].description);

    renderHomework(loadedLessons[num].events.HW);
    renderStuff(loadedLessons[num].events.AddStuff);
} 

///////////////////


function saveLesson() {
    // сохранение через ajax
    sendReq(
        "POST",
        {
            "action": "teachLesson",
            "lessonId":loadedLessons[selLessonId].id,
            "theme": $("#inpName").val(),
            "description": $("#inpDescr").val()
        },
        function (data) {
            console.log(data);
            if (data=="200")
            {
            selectSubject(subjID, true)
            openSubjPlan(selLessonId);
            }

        }

    );
}
///////////////////
function addHw() {
    sendFileToServer("teachAddHw",
    selLessonId,
    $("#addHwName").val(),
    $("#addHwDescr").val(),
    $("#addHwFile")[0].files[0])
}
function addStuff() {
    sendFileToServer("teachAddStuff", lessonId, name, file, descr)
}
// 
function delHw(uid) {
    // TODO
    alert(uid);
}
function delStuff(uid) {
    // TODO
    alert(uid);
}
// ////////////////
// send file
// https://stackoverflow.com/questions/2320069/jquery-ajax-file-upload
function sendFileToServer(action, lessonId, name, file, descr) {
    var formData = new FormData();
    formData.append('action', action);
    formData.append('lessonId', lessonId);
    formData.append('name', name);
    formData.append('file', file);
    formData.append('descr', descr);

    formData.append('csrfmiddlewaretoken', ccrf);

    $.ajax({
        url : '/api/',
        type : 'POST',
        data : formData,
        async: true,
        processData: false,  // tell jQuery not to process the data
        contentType: false,  // tell jQuery not to set contentType
        success : function(data) {
            if (data=="200")
            openSubjPlan(selLessonId);
            console.log(data);
            
        }
 });
}