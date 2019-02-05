pipeline {
  agent any

  environment {
    ANSIBLE_PATH='_infra/ansible/'
    DJANGO_SETTINGS_MODULE='landscape.settings'
  }

  stages {
    stage('Prepare') {
      steps {
        sh '''
        set -e
        /opt/python37/bin/python3 -m venv _venv
        _venv/bin/pip install -e .[for_tests]
        _venv/bin/pip install devpi
        '''
      }
    }
    stage('Test') {
      steps {
        sh('# _venv/bin/nosetests weevils/tests.py')
      }
    }
    stage('Upload') {
      environment {
        DEVPI_PASSWORD = credentials('devpi_password')
      }
      steps {
        sh '''
        set -e
        _venv/bin/devpi use http://devpi:"${DEVPI_PASSWORD}@pypi.manage.redcliff.ltd
        _venv/bin/devpi login privpkg --password="${DEVPI_PASSWORD}"
        _venv/bin/devpi use privpkg/privpkg
        rm -rf dist
        python setup.py sdist
        devpi upload
        '''
      }
    }
  }
}
