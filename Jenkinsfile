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
                    script {
                    sh 'coverage run manage.py test -v 1 && coverage report'
                    step([$class: 'CoberturaPublisher', 
                        coberturaReportFile: "cov.xml",
                    ])
                    junit "pyunit.xml"
                    }
               }
          }
    }
}
