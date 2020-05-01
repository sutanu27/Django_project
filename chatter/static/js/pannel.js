
window.onclick=function(event) {
    if (!event.target.offsetParent.classList.contains('dropdown-contact'))
    this.app5.contacts=[]
}



function setActive(target_class){
    var btns = document.getElementsByClassName(target_class);
    var current = document.getElementsByClassName(target_class+" active");
    if(current.length!=0)
    current[0].className = current[0].className.replace(" active", "");
    for(i=0;i<btns.length;i++){
        if (btns[i].id==app5.currentChatRoomId){
            btns[i].className += " active";
            break;
        }
    }
}


var app1=new Vue({
    el:'#chat_pannel',
    delimiters: ['[{', '}]'],
    data:{
        active:'',
        chatroom_url:'http://'+window.location.host+'/api/v2/ChatRoom/',
        timer:null
    },
    methods: {
        renderChat(){
            axios.get(this.chatroom_url)
            .then(function(response){
                app.form=false;
                app.add_type="Group";
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
        },
        renderChatRepeated(){
            app1.timer=window.setInterval(() => {
                 app1.renderChat()
                 },500);
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
            app.form=false;
            app.add_type="Contact";
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
            setTimeout(() => { setActive("chat_box") }, 50);
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
            app.form=false;
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
    },
    methods:{
        switchToHomeProfile(){
            app5.displayProfile('');
        }        
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
        files:[],
        profile:null,
        contacts:[]
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
        saveEditedProfile(){
            var chatroom_url='http://'+window.location.host+'/api/v3/profileapi/';
            var name=app5.profile.data.name.split(' ')
            var f_name=''
            for(i=0;i<name.length-1;i++)
            f_name+=name[i]
            var l_name=name[name.length-1]
            var status=app5.profile.data.status
            let formData = new FormData();
            rawData={
                'host': {
                    "first_name": f_name,
                    "last_name": l_name,
                        },
                "status":status
                }
            rawData = JSON.stringify(rawData)
            formData.append('data',rawData );
            
            if(profile_image_file)
            formData.append('image',profile_image_file, profile_image_file.name);            
            let req = {
                url:chatroom_url,
                method: 'PUT',
                data:formData,
                headers: {'X-CSRFTOKEN': csrftoken,'Content-Type': 'multipart/form-data'}
              }          
            axios(req)
            .then( function(response){
            }).catch(function(error){
                console.log(error)
            })             
        },
        addToGroup(username){
            var chatroom_url='http://'+window.location.host+'/api/v2/chatroomapi/'+app5.currentChatRoomId
 
            let req = {
                url:chatroom_url,
                method: 'PUT',
                data: {
                    "newroomie":username
                },
                headers: {'X-CSRFTOKEN': csrftoken }
              }            
            axios(req)
            .then( function(response){
                app5.contacts=[];
                app5.displayDropdown();
            }).catch(function(error){
                console.log(error)
            })              
        },
        displayDropdown(){
            if(app5.contacts.length==0){
                var contact_url='http://'+window.location.host+'/api/v3/Contact/'+'?roomid='+app5.currentChatRoomId
                axios.get(contact_url)
                .then( function(response){
                    app5.contacts=[];
                    if(response.data.length==0)
                    app5.contacts.push({img_link:false, first_arg:'', second_arg:'Nothing to add'});
                    for(var i=0; i<response.data.length; i++){
                        var a=response.data[i];
                        app5.contacts.push({img_link:a.img_link, first_arg: a.full_name, second_arg:a.username});
                    }
                }).catch(function(error){
                    console.log(error)
                })    
            }else{
                app5.contacts=[]
            }
        },
        renderChatWindow(a){
            app.renderChatWindow({img_link:a.img_link, openchat:a.link , first_arg: a.name, second_arg:a.timestamp, is_group:a.is_group, has_room_id:true},null);
        },
        displayProfile(room_id){
            document.getElementsByClassName('loading')[0].classList=' loading'

            var api_url='http://'+window.location.host+'/api/v2/profile/'+room_id
            var is_self=false
            if (room_id=='')
            is_self=true
            axios.get(api_url)
            .then(function(response){
                app5.profile={
                   'data': response.data,
                   'is_self': is_self
                };
            }).catch(function(error){
                console.log(error);
            })
        },
        manageMessage(event){
            if(!event.shiftKey)
                this.sendMessage(event);
        },
        addFiles(event){
            this.files=[]
            for(var i=0;i<event.target.files.length;i++){
                this.files.push(event.target.files[i]);
            }
        },
        sendMessage(event){
            var is_file=this.files.length!=0
            var file_size=0
            var upload_status=''
            var file_name=''
            if(is_file){
//            app.chatSocket.send(this.files[0],{ binary: true });                                        
                var file_size=this.files[0].size;
                var upload_status='started';
                var file_name=this.files[0].name;
            }
            var rawData={
                'message_content': this.message_content,
                'is_file': is_file,
                'file_size':file_size,
                'upload_status':upload_status,
                'file_name':file_name
            }

            rawData = JSON.stringify(rawData)
            if(this.message_content!='' || this.files.length!=0){
                if(app.chatSocket){
                        app.chatSocket.send(rawData);
                        if (is_file)
                            app.chatSocket.send(this.files[0],{ binary: true });  
                            for( i=1;i<this.files.length;i++){
                                file_size=this.files[i].size;
                                upload_status='started';
                                file_name=this.files[i].name;
                
                                var blankrawData={
                                    'message_content': '',
                                    'is_file': is_file,
                                    'file_size':file_size,
                                    'upload_status':upload_status,
                                    'file_name':file_name
                                }
                                console.log(blankrawData);                    
                                app.chatSocket.send(JSON.stringify(blankrawData));
                                app.chatSocket.send(this.files[i],{ binary: true });  
                            }
                    }
                else{
                    alert("ChatRoom doesn't extst.\n Refresh this Page.");
                }
            }
            this.message_content=''
            this.files=[]
        }
    },
    updated() {
        setScroll()
      }

})




var app=new Vue({
    el:'#pannels',
    delimiters: ['[{', '}]'],
    components:{
        'chatbox-component':{
            props:['on_chatroom','chatindex'],
            methods:{
                renderChatWindow(arg){
                    app.renderChatWindow(arg)
                }
            },
            template:
        ` <div class="row chat_box  border " :id="on_chatroom.openchat">
                <div class="img_box ">
                    <img :src="on_chatroom.img_link"  class="rounded-circle border" width="45" height="45">
                </div>
                <a style="text-decoration: none;" class="detail_box container-fluid" v-on:click="renderChatWindow(on_chatroom )" >
                    <div class="row ">
                            <div class="box_top col-12">{{ on_chatroom.first_arg }}</div>
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
        chatSocket:null,
        add_type:'Group',
        form:false,
        group_name:'',
        first_name:'',
        last_name:'',
        username:''
    },  
    methods: {
        createContact(){
            var chatroom_url='http://'+window.location.host+'/api/v3/Contact/'

            let req = {
                url:chatroom_url,
                method: 'POST',
                data: {
                    "first_name":app.first_name,
                    "last_name":app.last_name,
                    "username":app.username
                },
                headers: {'X-CSRFTOKEN': csrftoken}
              } 
            axios(req)
            .then( function(response){
                app.group_name='';
                app1.renderChat();
            }).catch(function(error){
                console.log(error)
            })              
            
        },
        createGroup(){
            var chatroom_url='http://'+window.location.host+'/api/v2/chatroomapi/'
 
            let req = {
                url:chatroom_url,
                method: 'POST',
                data: {
                    "group_with_current_user":app.group_name
                },
                headers: {'X-CSRFTOKEN': csrftoken}
              }            
            axios(req)
            .then( function(response){
                app.group_name='';
                app1.renderChat();
            }).catch(function(error){
                console.log(error)
            })              
            
        },
        renderCreateGroup(){
            app.form=true;

        },
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
            document.getElementsByClassName('loading')[0].classList=' loading'

            if(!arg.has_room_id){
                this.findRoomId(arg)
            }
            else{
            app5.profile=null;
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
                        $('.chat_window').scrollTop($('.chat_window')[0].scrollHeight);
                    }
                }).catch(function(error){
                    console.log(error)
                })    

                if (app.chatSocket!=null)
                {
                    app.chatSocket.close()
                }
                this.chatSocket = new ReconnectingWebSocket(
                    'ws://' + window.location.host +
                    '/ws/chat/' + app5.currentChatRoomId + '/');
                    this.chatSocket.binaryType = "arraybuffer";

                this.chatSocket.onmessage = function(e) {
                    var data = JSON.parse(e.data).message;
                    app5.chatmessages.push({auther_name: data['auther'], is_send: data['auther']==user, time_stamp: data['timestamp'], content: data['content'], file_msg_link: data['file_msg_url']});    
                    app1.renderChat()
                };
                this.chatSocket.onclose = function(e) {
                    console.error('Chat socket closed unexpectedly');
                };
                setActive('chat_box')
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
        app1.renderChat();
        app5.displayProfile('');
    },
    updated(){
        setActive('chat_box')
        document.getElementsByClassName('loading')[0].classList+=' hide';  
    }
})


