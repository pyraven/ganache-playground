# Networking
########################################

resource "google_compute_subnetwork" "vpc-subnet" {
  name          = "playground-subnetwork"
  ip_cidr_range = var.vpc_cidr_block
  region        = var.region
  network       = google_compute_network.vpc-network.id
}

resource "google_compute_network" "vpc-network" {
  name                    = "playground-vpc"
  auto_create_subnetworks = "false"
}

# Firewalls
########################################

resource "google_compute_firewall" "playground-allow-ssh" {
  name    = "allow-ssh"
  network = google_compute_network.vpc-network.id

  allow {
    protocol = "tcp"
    ports    = ["22", "9000"]
  }

  source_ranges = [var.source-ip]
  source_tags   = ["allow-access"]
}

# Computing
########################################

resource "tls_private_key" "ssh_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "google_compute_instance" "playground-vm" {
  name         = "playground-vm"
  machine_type = "e2-medium"
  zone         = var.zone

  tags = ["allow-access"]

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2004-lts"
      size  = 50
    }
  }

  network_interface {
    subnetwork = google_compute_subnetwork.vpc-subnet.self_link

    access_config {}
  }

  metadata = {
    enable-oslogin = "TRUE"
    ssh-keys       = "ubuntu:${tls_private_key.ssh_key.public_key_openssh} ubuntu"
  }

  connection {
    host        = google_compute_instance.playground-vm.network_interface.0.access_config.0.nat_ip
    type        = "ssh"
    user        = "ubuntu"
    timeout     = "500s"
    private_key = tls_private_key.ssh_key.private_key_pem
    agent       = false
  }

  provisioner "file" {
    source      = "setup/setup.sh"
    destination = "/tmp/setup.sh"
  }

  provisioner "file" {
    source      = "setup/start.sh"
    destination = "/tmp/start.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/setup.sh /tmp/start.sh",
      "sh /tmp/setup.sh",
      "sh /tmp/start.sh",
      "sleep 10"
    ]
  }
}

# Output
########################################

output "external_ip" {
  value = "nc -vz ${google_compute_instance.playground-vm.network_interface.0.access_config.0.nat_ip} 9000"
}
########################################
