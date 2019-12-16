$(document).ready(function() {
    select_option_content = "";
    for (var i = 0; i < course_types.length; ++i) {
        select_option_content += "<option>" + course_types[i] + "</option>";
    }

    $("#course_types").html(select_option_content);
});