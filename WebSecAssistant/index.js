// chrome.tabs.query({active: true, currentWindow: true},function(tabs){   
//   var currentTab = tabs[0];
//   makeRequestCurrentUrl(currentTab.url,'website')
// });
// chrome.downloads.search({limit: 5}, function(data) {
//     data.forEach(function(item, i) {
//         var fname = getFileName(item.filename);
//         $('#table').find('tbody').append("<tr><td>"+fname+"</td><td><button class='btn btn-secondary actionButton' rel='"+item.filename+"' id='"+i+"'>Button</button></td><td><span id='response_"+i+"'></span></td></tr>");
      
//     });
//     $('#table').find('tbody').append("<tr><td><a style='cursor:pointer' id='showmore' class='dynamicElement link'>Show more</a></td></tr>");
// });
// chrome.downloads.search({limit: 1000}, function(data) {
//     data.forEach(function(item, i) {
//         if(i>=5){ 
//            var fname = getFileName(item.filename);
//           $('#table').find('tbody').append("<tr style='display:none' class='more'><td>"+fname+"</td><td><button class='btn btn-secondary actionButton' rel='"+item.filename+"' id='"+i+"'>Button</button></td><td><span id='response_"+i+"'></span></td></tr>");

//         }
      
//     });
   
// });

// $(function() {
//      //var u = decodeURIComponent(window.location.search.match(/(\?|&)u\=([^&]*)/)[2]);
   
//    // makeRequest(u,'website');

//     $(document).on("click", '#showmore', function() {
//       $('.more').show();
//       $('#showmore').hide();
        
//     });
//     $(document).on("click", '.actionButton', function() {
//        var id = $(this).attr('id');
//        var rel = $(this).attr('rel');
       
//        makeRequest(rel,id)

        
//     });

// });
// function getFileName(fullPath){
//   var filename = fullPath.replace(/^.*[\\\/]/, '');
//   return filename;

// }
// function makeRequest(rel,ids){
//   $.ajax({
//     type: "POST",
//     url: 'http://127.0.0.1/fyp/virus.php',
//     data: {
//       curl: rel
//   },
//   success: function (responseText) {
    
//      $("#response_"+ids).html(responseText)
//   },
//   error: function (jxhr) {
//     alert(jxhr.responseText);
//   }

//   });
// }
// function makeRequestCurrentUrl(rel,ids){
//   $.ajax({
//     type: "POST",
//     url: 'http://127.0.0.1/fyp/phis.php',
//     data: {
//       curl: rel
//   },
//   success: function (responseText) {
    
//      $("#response_"+ids).html(responseText)
//   },
//   error: function (jxhr) {
//     alert(jxhr.responseText);
//   }

//   });
// }


chrome.downloads.search({limit: 5}, function(data) {
  data.forEach(function(item, i) {
      var fname = getFileName(item.filename);
      $('#table').find('tbody').append("<tr><td>"+fname+"</td><td><button class='btn btn-secondary actionButton' rel='"+item.filename+"' id='"+i+"'>Verify</button></td><td><span id='response_"+i+"'></span></td></tr>");
    
  });
  $('#table').find('tbody').append("<tr><td><a style='cursor:pointer' id='showmore' class='dynamicElement link'>Show more</a></td></tr>");
});
chrome.downloads.search({limit: 10000}, function(data) {
  data.forEach(function(item, i) {
      if(i>=5){ 
         var fname = getFileName(item.filename);
        $('#table').find('tbody').append("<tr style='display:none' class='more'><td>"+fname+"</td><td><button class='btn btn-secondary actionButton' rel='"+item.filename+"' id='"+i+"'>Verify</button></td><td><span id='response_"+i+"'></span></td></tr>");

      }
    
  });
 
});
chrome.tabs.query({active: true, currentWindow: true},function(tabs){   
var currentTab = tabs[0];
makeRequestCurrentUrl(currentTab.url,'website')
});
$(function() {
   //var u = decodeURIComponent(window.location.search.match(/(\?|&)u\=([^&]*)/)[2]);
 
 // makeRequest(u,'website');

  $(document).on("click", '#showmore', function() {
    $('.more').show();
    $('#showmore').hide();
      
  });
  $(document).on("click", '.actionButton', function() {
     var id = $(this).attr('id');
     var rel = $(this).attr('rel');
     
     makeRequest(rel,id)

      
  });

});
function getFileName(fullPath){
var filename = fullPath.replace(/^.*[\\\/]/, '');
return filename;

}
function makeRequest(rel,ids){
$.ajax({
  type: "POST",
  url: 'http://127.0.0.1/WebSecAsst/virus.php',
  data: {
    curl: rel
},
success: function (responseText) {
  
   $("#response_"+ids).html(responseText)
},
error: function (jxhr) {
  alert(jxhr.responseText);
}

});
}
function makeRequestCurrentUrl(rel,ids){
$.ajax({
  type: "POST",
  url: 'http://127.0.0.1/WebSecAsst/phis.php',
  data: {
    curl: rel
},
success: function (responseText) {
  
   $("#response_"+ids).html(responseText)
},
error: function (jxhr) {
  alert(jxhr.responseText);
}

});
}