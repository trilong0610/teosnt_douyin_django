$(document).ready(function(){
    $("#btn-video").click(function(e) {
        e.preventDefault();
        // Kiem tra input code
        let code = $("#code-active").val()
        if (!code){ //Khong tim thay code
            showToastr(get_notification("error","Lỗi","Vui lòng nhập code"))
        }
        else{ // Tim thay code
            // Kiem tra code con han ko
            $.ajax({
               type: "GET",
               url: '/check_code/' + $("#code-active").val().toString(),
               success: function(data)
               {
                    if("success" in data){ // Key con` han
                       e.preventDefault(); // avoid to execute the actual submit of the form.

                        let input = $("#url-video").val();
                        // Kiem tra du lieu
                        if(!input){
                            showToastr({"tag" : "error","title": "Lỗi","data": "Vui lòng nhập URL video"});
                            return;
                        }

                        // Kiem tra dinh dang url
                        let url_reg = new RegExp('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+');
                        if(!url_reg.test(input)){
                            showToastr({"tag" : "error","title": "Lỗi","data": "Không tìm thấy URL"});
                            return;
                        }

                        // kiem tra co dung url video khong
                        let douyin_reg = new RegExp('https://v.douyin.com');
                        if(!douyin_reg.test(input)){
                            showToastr({"tag" : "error","title": "Lỗi","data": "URL video không đúng định dạng"});
                            return;
                        }
                        showToastr(get_notification("success","","Đang tải video"))
                        $("#form-video").submit();
                    }
                    else{ // Key het han
                        showToastr(data)
                    }
               },
                error: function (data) {
                    showToastr(get_notification("error","","Đã xảy ra lỗi \n Vui lòng thử lại"))
                },
             });

        }

    });

    $("#btn-code").click(function(e) {

        e.preventDefault(); // avoid to execute the actual submit of the form.
        showToastr(get_notification("warning", " ", "Đang lấy code.\nVui lòng đợi"))
        $('#div-get-file').empty();
        $.ajax({
            type: "GET",
            url: "/create_code/",
            success: function (data) {
                showToastr(data);
                if ("link1s" in data) {
                    let btnGetFile = $('<a href=' + data.link1s + ' target="_blank" rel="noopener noreferrer"><button id="btn-get-code" class="btn btn-danger btn-block text-white btn-user" style="margin-top: 20px;">Lấy code tại đây</button><!-- End: btn-login --></a>');

                    $('#div-get-file').delay(1000).append(btnGetFile);

                }
                else {
                    $('#div-get-file').empty();
                }
            },
            error: function (data) {
                showToastr(data);
            },
        });
    });

    function showToastr(data) {
    let i = -1,
        toastCount = 0,
        $toastlast,
        getMessage = function () {
            let msgs = ['Hello, some notification sample goes here',
                '<div><input class="form-control input-small" value="textbox"/>&nbsp;<a href="http://themeforest.net/item/metronic-responsive-admin-dashboard-template/4021469?ref=keenthemes" target="_blank">Check this out</a></div><div><button type="button" id="okBtn" class="btn blue">Close me</button><button type="button" id="surpriseBtn" class="btn default" style="margin: 0 8px 0 8px">Surprise me</button></div>',
                'Did you like this one ? :)',
                'Totally Awesome!!!',
                'Yeah, this is the Metronic!',
                'Explore the power of App. Purchase it now!'
            ];
            i++;
            if (i === msgs.length) {
                i = 0;
            }

            return msgs[i];
        };

    let shortCutFunction = data.tag;
    let msg = data.data;
    let title = data.title || '';

    let toastIndex = toastCount++;

    toastr.options = {
        closeButton: "checked",
        positionClass: 'toast-top-right',
        onclick: null,
        showDuration: 1000,
        hideDuration:1000,
        timeOut : 2000,
        extendedTimeOut : 1000
    };

    toastr.options.showEasing = "swing";
    toastr.options.hideEasing = "linear";
    toastr.options.showMethod = "fadeIn";
    toastr.options.hideMethod = "fadeOut";


    if (!msg) {
        msg = getMessage();
    }
    let $toast = toastr[shortCutFunction](msg, title); // Wire up an event handler to a button in the toast, if it exists

}

    function get_notification(tag, title, data){
        return {"tag": tag, "title": title, "data": data}
    }
});



//--------END CROP AVATAR---------