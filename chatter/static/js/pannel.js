

var app1=new Vue({
    el:'#chat_pannel',
    delimiters: ['[{', '}]'],
    data:{
        active:'',
        chatroom_url:'http://'+window.location.host+'/api/v2/ChatRoom/'
    },
    methods: {
        renderChat(){
            axios.get(this.chatroom_url)
            .then(function(response){
                app.is_search=false;
                app.user_sub_str="";
                app.chatrooms=[];
                app1.active="active";
                app2.active="";
                app3.active="";
                for(var i=0; i<response.data.length; i++){
                    var a=response.data[i];
                    app.chatrooms.push({img_link:a.img_link, openchat:a.link , first_arg: a.name, second_arg:a.timestamp, is_group:a.is_group, has_room_id:true});
                }
            }).catch(function(error){
                console.log(error)
            })
        }
    }
})


var app2=new Vue({
    el:'#contact_pannel',
    delimiters: ['[{', '}]'],
    data:{
        active:'',
        chatroom_url:'http://'+window.location.host+'/api/v3/Contact/'
    },
    methods: {
        renderContact(){
            app1.active="";
            app2.active="active";
            app3.active="";
            app.is_search=false;
            app.user_sub_str="";
            axios.get(this.chatroom_url)
            .then(function(response){
                app.chatrooms=[];
                for(var i=0; i<response.data.length; i++){
                    var a=response.data[i];
                    app.chatrooms.push({img_link:a.img_link, openchat:a.username , first_arg: a.full_name, second_arg:a.username,has_room_id:false, is_group:false});
                }
            }).catch(function(error){
                console.log(error)
            })
        }
    }
})

var app3=new Vue({
    el:'#search_pannel',
    delimiters: ['[{', '}]'],
    data:{
        active:'',
    },
   methods: {
        renderSearch(){
            app.is_search=true;
            app.user_sub_str="";
            app1.active="";
            app2.active="";
            app3.active="active";
           app.chatrooms=[];
        }
    }
})

var app4=new Vue({
    el:'#nav_list',
    delimiters: ['[{', '}]'],
    data:{
        currentTab:'Home',
    }
})


var app5=new Vue({
    el:'#main',
    delimiters: ['[{', '}]'],
    data:{
        currentChatRoomId:'',
        currentChatRoomName:'',
        currentChatRoomImage:'',
        is_group:false,
        chatmessages:[],
        message_content:'',
        files:[]
    },
    components:{
        'message-component':{
            props:['chatmessage','is_group'],
            template:
    `   <div class="row">
            <div class="col-12">
                <div :class="chatmessage.is_send? 'send':'receive'" class="container-fluid">
                    <div class="row auther" v-show="!chatmessage.is_send && is_group"> {{ chatmessage.auther_name }} </div>
                    <div class="row  content"> {{chatmessage.content}} </div>
                    <div v-show="chatmessage.file_msg_link !=''" class="row file_box">
                        <img  class="file_link" :src="chatmessage.file_msg_link" >  
                    </div>
                    <div class="row timebox"> 
                        <div class='time'>{{ chatmessage.time_stamp }} </div>
                    </div>
                </div>    
            </div>
        </div>`
        }
    },
    methods:{
        manageMessage(event){
            if(!event.shiftKey)
                this.sendMessage(event);
        },
        addFiles(event){
            this.files=[]
            for(var i=0;i<event.target.files.length;i++){
                this.files.push(event.target.files[0]);
            }
        },
        sendMessage(event){
            var is_file=this.files.length!=0

            if(this.message_content!='' || is_file  ){
                if(app.chatSocket){

                        app.chatSocket.send(JSON.stringify({
                            'message_content': this.message_content,
                            'is_file': is_file,
                            'file': ''
                        }));
                }
                else{
                    alert("ChatRoom doesn't extst.\n Refresh this Page.");
                }
            }
            this.message_content=''
        },
        sendFile(file) {
            var reader = new FileReader();
            var rawData = new ArrayBuffer();            
            reader.loadend = function() {

            }
            reader.onload = function(e) {
                rawData = e.target.result;
                ws.send(rawData);
                alert("the File has been transferred.")
            }
            reader.readAsArrayBuffer(file);
        }
    },
    updated: function () {
        setScroll()
      }    

})




var app=new Vue({
    el:'#pannels',
    delimiters: ['[{', '}]'],
    components:{
        'chatbox-component':{
            props:['on_chatroom'],
            methods:{
                renderChatWindow(arg){
                    app.renderChatWindow(arg)
                }
            },
            template:
        ` <div class="row chat_box  border">
                <div class="img_box ">
                    <img :src="on_chatroom.img_link"  class="rounded-circle border" width="45" height="45">
                </div>
                <a style="text-decoration: none;" class="detail_box container-fluid" v-on:click="renderChatWindow(on_chatroom )" >
                    <div class="row ">
                            <div class="box_top col-12"><b>{{ on_chatroom.first_arg }}</b></div>
                            <div class="box_bottom col-12">{{ on_chatroom.second_arg }}</div>
                    </div>
                </a>
            </div>`
        },
        'searchbar-component':{
            props:['value',],
            methods:{
                onRenderSearchNames(){
                    app.renderSearchNames()
                }
            },
            template:
        `<div class='search_class'>
            <div class="input-group">
                <input type="text" class="inline_a" placeholder="Search.." name="username_substring"  :value="value" @input="$emit('input', $event.target.value)" @keyup="onRenderSearchNames" />
                <button class="input-group-addon inline_b"><i class="fa fa-search"></i></button>
             </div>
        </div>`
        },
    },
    data:{
        is_search:false,
        user_sub_str:"",
        chatroom_url:'http://'+window.location.host+'/api/v1/findusers/',
        message_url:'http://'+window.location.host+'/api/v2/messages/?roomid=',
        chatroom_find_url:'http://'+window.location.host+'/api/v2/ChatRoom/',
        chatrooms:[],
        chatSocket:null
    },  
    methods: {
        renderSearchNames(){
            var c_url=this.chatroom_url+app.user_sub_str
            axios.get(c_url)
            .then(function(response){
                app.chatrooms=[];
                for(var i=0; i<response.data.length; i++){
                    var a=response.data[i];
                    app.chatrooms.push({img_link:a.img_link, openchat:a.username , first_arg: a.username, second_arg:a.full_name,has_room_id:false, is_group:false});
                }
            }).catch(function(error){
                console.log(error)
            })
        },
        renderChatWindow(arg){
            if(!arg.has_room_id){
                this.findRoomId(arg)
            }
            else{
            app5.currentChatRoomId=arg.openchat;
            app5.currentChatRoomName=arg.first_arg;
            app5.currentChatRoomImage=arg.img_link;
            app5.is_group=arg.is_group;
            app5.has_room_id=arg.has_room_id

                var m_url=this.message_url+app5.currentChatRoomId;
                axios.get(m_url)
                .then(function(response){
                    app5.chatmessages=[];
                    for(var i=0; i<response.data.length; i++){
                        var a=response.data[i];
                        app5.chatmessages.push(a);
                    }
                }).catch(function(error){
                    console.log(error)
                })    
                this.chatSocket = new ReconnectingWebSocket(
                    'ws://' + window.location.host +
                    '/ws/chat/' + app5.currentChatRoomId + '/');
                    this.chatSocket.binaryType = "arraybuffer";

                this.chatSocket.onmessage = function(e) {
                    var data = JSON.parse(e.data).message;
                    if(e.data.has_file){
                        app5.sendFile(data['id'],app5.files)
                    }
                    else{
                        app5.chatmessages.push({auther_name: data['auther'], is_send: true, time_stamp: data['timestamp'], content: data['content'], file_msg_link: data['file_msg_url']});    
                    }
                };
                
                this.chatSocket.onclose = function(e) {
                    console.error('Chat socket closed unexpectedly');
                };
            }            
        },
        findRoomId(arg){
            axios.get(this.chatroom_find_url+arg.openchat)
            .then(function(response){
                arg.openchat=response.data.link;
                arg.has_room_id=true;
                app.renderChatWindow(arg)
            }).catch(function(error){
                console.log(error)
            })
        }
    },
    mounted(){
        app1.renderChat()
    }
})


