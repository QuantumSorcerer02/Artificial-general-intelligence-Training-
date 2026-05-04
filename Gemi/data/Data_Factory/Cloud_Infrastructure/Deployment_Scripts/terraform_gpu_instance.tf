# Terraform Configuration for Astral Bloom Cloud Node (Gemma Fine-tuning)
provider "google" {
  project = "quantum-nano-os"
  region  = "us-central1"
  zone    = "us-central1-a"
}

resource "google_compute_instance" "astral_bloom_gpu_node" {
  name         = "astral-bloom-training-node"
  machine_type = "a2-highgpu-1g" # A100 GPU instance for rapid fine-tuning

  boot_disk {
    initialize_params {
      image = "deeplearning-platform-release/common-cu113-debian-10"
      size  = 100
      type  = "pd-ssd"
    }
  }

  network_interface {
    network = "default"
    access_config {
      # Ephemeral IP
    }
  }

  guest_accelerator {
    type  = "nvidia-tesla-a100"
    count = 1
  }

  scheduling {
    on_host_maintenance = "TERMINATE" # Required for GPU instances
  }

  metadata_startup_script = <<-EOF
    #!/bin/bash
    echo "Bootstrapping Astral Bloom Cloud Node..."
    # Install dependencies
    pip3 install torch transformers accelerate huggingface_hub
    echo "Node Ready for Quantum Nano OS Sync."
  EOF
}