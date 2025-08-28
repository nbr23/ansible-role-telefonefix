@Library('jenkins-shared-library') _

pipeline {
    agent any

    stages {
        stage('Install role') {
          steps {
              sh 'ansible-galaxy role install -f git+$(echo $GIT_URL | sed "s|https://git.23.tf|ssh://git@git.23.tf:2323|")'
          }
        }
        stage('Sync github repo') {
            when { branch 'master' }
            steps {
                syncRemoteBranch('git@github.com:nbr23/ansible-role-telefonefix.git', 'master')
            }
        }
    }
}
