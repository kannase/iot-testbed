pipeline {
    agent {
        label 'worker-primary'
    }

    environment {
        // Using the internal Podman gateway to find the Mosquitto container
        MQTT_BROKER = 'localhost:1883'
		PYTHONPATH = "${WORKSPACE}"
    }

    stages {
        stage('1. Environment Setup') {
            steps {
                echo "Creating Virtual Environment and installing dependencies..."
                // Creates a local 'venv' folder and installs requirements 
                bat '''
                python -m venv venv
                .\\venv\\Scripts\\pip install -r requirements.txt
                '''
            }
        }

        stage('2. Provision Broker') {
            steps {
                echo "Ensuring Mosquitto Broker is running..."
                // This starts the broker container using the podman installed in your agent
                bat 'podman run -d --name mqtt-broker -p 1883:1883 eclipse-mosquitto || exit 0'
            }
        }

        stage('3. Integration Testing') {
            parallel {
                stage('Device Simulation') {
                    steps {
                        echo "Starting Device Simulator from subfolder..."
                        // Added 20-seconds timeout to stop the 'while True' loop eventually 
                        timeout(time: 20, unit: 'SECONDS') {
                            bat ".\\venv\\Scripts\\python.exe simulator/iot_device_simulator.py --broker %MQTT_BROKER% < nul || exit 0"
                        }
                    }
                }
                stage('Pytest Logic') {
                    steps {
                        echo "Running Pytest from subfolder..."
                        // Points to the exact folder: iot-testbed/tests/pytest 
                        bat ".\\venv\\Scripts\\python.exe -m pytest tests/pytest --junitxml=results.xml"
                    }
                }
				stage('Robot Framework E2E') {
                    steps {
                        echo "Running Robot Framework..."
                        script {
                            // Ensure directory exists so the robot plugin has a path to scan
                            bat 'if not exist robot_results mkdir robot_results'
                            
                            // If tests fail, this 'bat' command returns a non-zero exit code
                            // The pipeline will skip remaining steps and jump to 'post'
                            bat ".\\venv\\Scripts\\python.exe -m robot --outputdir robot_results tests/robot/iot_integration_test.robot"
                        }
                    }
                }
            }
        }
    }

  post {
    always {
        echo "Archiving All Test Results..."
        // 1. Existing Pytest Results
        junit 'results.xml'
		script {
            // 2. Professional Robot Plugin Results
            // This step is ONLY available because you installed the plugin!
            robot(
                outputPath: 'robot_results',   // Folder where your 'bat' command puts results
                logFileName: 'log.html',
                outputFileName: 'output.xml',
                reportFileName: 'report.html',
                passThreshold: 100.0,          // Build turns red if pass rate < 100%
                unstableThreshold: 80.0,       // Build turns yellow if pass rate < 80%
                onlyCritical: false            // Includes all tests in the statistics
            )
         }
    }
	 cleanup {
            // Step 2: Shutdown the hardware/containers
            bat 'podman stop mqtt-broker || exit 0'
            bat 'podman rm mqtt-broker || exit 0'
        }
   }
}
