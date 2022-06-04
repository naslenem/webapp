pipeline {
     agent {
          docker {
               image "python-image:3"
     	  }
     }
     triggers {
          pollSCM('* * * * *')
     }
     stages {
          stage("Compile") {
               steps {
                    sh "./test.sh"
               }
          }
          stage("Unit test") {
               steps {
                    sh "./test.sh"
               }
          }
          stage('Initialize'){
          steps {
          script{
                            def dockerHome = tool 'default-docker'
        env.PATH = "${dockerHome}/bin:${env.PATH}"
               }
               }

    }

          stage("Docker build") {
          
          	steps {
          	     sh "docker build -t localhost:5000/python-image ."
          	}
          }
    }
}
