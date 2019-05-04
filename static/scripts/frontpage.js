$(document).ready(function(){
/*   var webcontrolMessage = document.getElementById('webcontrolMessage');
   var webmcpMessage = document.getElementById('uiMessage');
   webcontrolMessage.scrollTop = webcontrolMessage.scrollHeight;
   webmcpMessage.scrollTop = webmcpMessage.scrollHeight;
   */
});

function requestPage(page, args=""){
  console.log("requesting page..")
  socket.emit('requestPage',{data:{page:page, isMobile:isMobile, args:args}});
}