variable "render_api_key" {
  type        = string
  description = "Render API key"
  sensitive   = true
}

variable "service_name" {
  type        = string
  description = "Name of your Render service"
}

variable "repo_url" {
  type        = string
  description = "Public GitHub repo URL"
}
