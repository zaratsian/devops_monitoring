resource "google_compute_instance" "default" {
  count        = "${var.num_nodes}"
  name         = "${var.name}-${count.index + 1}"
  machine_type = "f1-micro"
  zone         = "us-central1-a"

  tags = ["monitoring-test"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
    }
  }

  network_interface {
    network = "default"

    access_config {
        network_tier = "STANDARD"
    }
  }

  metadata_startup_script = <<-EOT
#! /bin/bash
sudo apt-get install -y python-pip
pip install flask psutil
adduser --disabled-password --gecos "" ztest
su - ztest
wget https://raw.githubusercontent.com/zaratsian/devops_monitoring/master/prometheus_exporter.py
python prometheus_exporter.py &
EOT

  service_account {
    scopes = ["userinfo-email", "compute-ro", "storage-ro"]
  }

}
