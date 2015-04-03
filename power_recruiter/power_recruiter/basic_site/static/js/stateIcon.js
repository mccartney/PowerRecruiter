var stateIcon = function (imgSource, content, type, candidate_id, candidate_name) {
    this.imgSource = imgSource;
    this.content = content;
    this.type = type;
    this.candidate_id = candidate_id;
    this.candidate_name = candidate_name;

    this.googleLink = function() {
        return "http://google.pl/#q=" + this.candidate_name + " " + this.type;
    }

    this.imageTag = function() {
        iconHiddenClass = "";
        if (this.content == null) {
            iconHiddenClass = " icon-hidden";
        }
        return '<img class="source-icon' + iconHiddenClass + '" src="' + this.imgSource+ '">';
    }

    this.mailLink = function() {
        hrefLink = "mailto:" + this.content;
        if (this.content == null) {
            hrefLink = "#";
        }
        return '<a href="'+ hrefLink + '">' + this.imageTag() + '</a>';
    }

    this.socialLink = function() {
        hrefLink = this.content;
        if (hrefLink == null) {
            hrefLink = this.googleLink();
        }
        return '<a href="' + hrefLink + '">' + this.imageTag() + '</a>';
    }

    this.toString = function() {
        if (type == 'email'){
            return this.mailLink();
        }
        return this.socialLink();
    }

}
