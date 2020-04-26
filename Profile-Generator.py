class Profile:
       
    def generateProfile():
        name    = ""
        surname = ""
        twitter = ""
        website = ""
        while(name == ""):
            name = input("Your name: ")
        while(surname == ""):
            surname = input("Your surname: ")
        print("\nThe following fields are not required but they are highly recommended!\n")
        website = input("Your website\n(Example: http://google.com): ")
        twitter = input("Your Twitter username: ")
        facebook = input("Your Facebook username/ID: ")
        github = input("Your GitHub username: ")
        googlePlus = input("Your Google+ username/ID: ")

        file = open(name.lower() + "-" + surname.lower() + ".html","w")
        file.write('<html>\n')
        file.write('<head>\n')
        file.write('<title>About ' + name + ' ' + surname + '</title>\n')
        file.write('<style>' + Profile.makeCSS() + '</style>\n')
        file.write('</head>\n')
        file.write('<body>\n')
        file.write('<div id="container">\n')
        file.write('<h1>' + name + ' ' + surname + '</h1>\n')
        
        if(twitter != ""):
            file.write('<h2><a href="https://twitter.com/' + twitter + '" target="_blank">Twitter</a></h2>\n')
        if(github != ""):
            file.write('<h2><a href="https://github.com/' + github + '" target="_blank">GitHub</a></h2>\n')
        if(website != ""):
            file.write('<h2><a href="' + website + '" target="_blank">Web site</a></h2>\n')
        if(facebook != ""):
            file.write('<h2><a href="https://facebook.com/' + facebook + '" target="_blank">Facebook</a></h2>\n')
        if(googlePlus != ""):
            file.write('<h2><a href="https://plus.google.com/u/0/' + googlePlus + '" target="_blank">Google Plus</a></h2>\n')
        file.write('</body>\n')
        file.write('</html>')
        file.close()

        print("\n" + name.lower() + "-" + surname.lower() + ".html has been created!")

    def makeCSS():
        css = "\n"
        css += "@import url('http://fonts.googleapis.com/css?family=Open+Sans:400,300,600');\n"
        css += "body{background-color:whitesmoke; background:url('http://www.giuseppesanfrancesco.it/templates/ja_t3_blank/themes/sito/images/bg-pattern.png');}\n"
        css += "#container{margin:30px auto 0px auto; width:900px; text-align:center;}\n"
        css += "h1{font-family:'Open Sans';}\n"
        css += "h2{font-weight:normal; font-family:'Open Sans';}\n"
        css += "a{color:royalblue; text-decoration:none; transition:color ease-out 1s;-webkit-transition: color ease-out 1s;}\n"
        css += "a:hover{color:red; transition:color ease-out 1s; -webkit-transition:color ease-out 1s;}"
        css += "\n"
        return css

if __name__ == '__main__':
    me = Profile
    me.generateProfile()