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
          stage("Code coverage") {
               steps {
		     sh "./test.sh"
               }
          }
    }
}
