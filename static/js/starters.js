$(document).ready(function() {
    html_content = "";
    for(var i = 0; i < starters.length; ++i) {
        html_content += "<div class=\"card\" style=\"width: 100%; float: left; margin-top: 2rem; margin-left: 2rem; margin-bottom: 2rem;\">";
        html_content += "<div class=\"card-body\">";
        html_content += "<h5 class=\"card-title\">" + starters[i]["name"] + "</h5>";
        html_content += "<p class=\"card-text\">";
        html_content += "<table class=\"table table-bordered\">";
        
        html_content += "<tr>";
        html_content += "<th>Course Type</th>";
        html_content += "<td>" + starters[i]["course_type"] + "</td>";
        html_content += "</tr>";

        html_content += "<tr>";
        html_content += "<th>Prep Time</th>";
        html_content += "<td>" + starters[i]["prep_time"] + "</td>";
        html_content += "</tr>";

        html_content += "<tr>";
        html_content += "<th>Cooking Time</th>";
        html_content += "<td>" + starters[i]["cooking_time"] + "</td>";
        html_content += "</tr>";

        html_content += "<tr>";
        html_content += "<th>Ingredients</th>";
        html_content += "<td>" + starters[i]["ingredients"] + "</td>";
        html_content += "</tr>";

        html_content += "<tr>";
        html_content += "<th>Makes</th>";
        html_content += "<td>" + starters[i]["makes"] + "</td>";
        html_content += "</tr>";

        html_content += "<tr>";
        html_content += "<th>Description</th>";
        html_content += "<td>" + starters[i]["description"] + "</td>";
        html_content += "</tr>";

        html_content += "<tr>";
        html_content += "<th>Method</th>";
        html_content += "<td>" + starters[i]["method"] + "</td>";
        html_content += "</tr>";

        html_content += "</table>";
        html_content += "</p>";
        html_content += "</div>";
        html_content += "</div>";
    }
    $("#starters-items-list").html(html_content);
});