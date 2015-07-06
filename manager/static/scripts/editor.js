/* Copyright 2012 Ivebo.
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.*/
$(document).ready(function(){
    tinyMCE.init({
    mode : "exact",
    convert_urls : false,
    elements : "contentpage",
    theme : "advanced",
    plugins : "pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template,wordcount,advlist,autosave,inlinepopups",
    theme_advanced_buttons1 : "cut,copy,paste,pastetext,pasteword,separator,search,replace,blockquote,separator,bold,italic,underline,sub,sup,|,strikethrough,justifyleft,justifycenter,justifyright, justifyfull,separator,bullist,numlist,outdent,indent,undo,redo,link,unlink,anchor,image,cleanup,code",
    theme_advanced_buttons2 : "table,tablecontrols,|,insertlayer,moveforward,movebackward,absolute,|,insertdate,inserttime,hr,charmap",
    theme_advanced_buttons3 : "styleselect,formatselect,fontselect,fontsizeselect,forecolor,backcolor",
    theme_advanced_toolbar_location : "top",
    theme_advanced_toolbar_align : "left",
    theme_advanced_statusbar_location : "bottom",
    //forced_root_block : false,
    extended_valid_elements : "iframe[src|style|width|height|scrolling|marginwidth|marginheight|frameborder],script[type|src]",
    /*content_css : "/static/css/base.css"//Css del sitio*/
    /*setup : function(ed) {
        // Add a custom button
        ed.addButton('prueba', {
            title : 'My Borton',
            image : 'img/example.gif',
            onclick : function() {
                                // Add you own code to execute something on click
                                ed.focus();
                ed.selection.setContent('Hello world!');
            }
        });
    }*/
    }); 
});