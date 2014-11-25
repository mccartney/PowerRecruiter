var stateIcon = function (imgSource, content, type, candidateId, candidateName) {
    this.imgSource = imgSource;
    this.content = content;
    this.type = type;
    this.candidateId = candidateId;
    this.candidateName = candidateName;

    this.googleLink = function() {
        return "http://google.pl/#q=" + this.candidateName + " " + this.type;
    }

    this.socialLink = function() {
        hrefLink = this.content;
        if (hrefLink == null) {
            hrefLink = this.googleLink();
        }
        return "<a href ='" + hrefLink + "'>" + this.imageTag() + "</a>";
    }

    this.imageTag = function() {
        iconHiddenClass = "";
        if (this.content == null)
            iconHiddenClass = "icon-hidden";
        return '<img class="source-icon ' + iconHiddenClass + '" src="' + this.imgSource+ '">';
    }

    this.mailLink = function() {
        hrefLink = "mailto:" + this.content;
        if (this.content == null) {
            hrefLink = "#";
        }
        return "<a href ='" + hrefLink + "'>" + this.imageTag() + "</a>";
    }

    this.toString = function() {
        if (type == 'email')
            return this.mailLink();
        return this.socialLink();
    }

}
