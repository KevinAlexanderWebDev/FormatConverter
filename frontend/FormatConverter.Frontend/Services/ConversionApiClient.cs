using System.Net.Http.Json;

namespace FormatConverter.Frontend.Services {
    public class ConversionApiClient {
        private readonly HttpClient _httpClient;

        public ConversionApiClient(HttpClient httpClient) {
            _httpClient = httpClient;
        }

        public async Task<byte[]> ConvertAsync(Stream fileStream, string fileName, string toFormat = "pdf") {
            using var content = new MultipartFormDataContent();

            var fileContent = new StreamContent(fileStream);
            fileContent.Headers.ContentType = new System.Net.Http.Headers.MediaTypeHeaderValue("application/octet-stream");
            content.Add(fileContent, "file", fileName);
            content.Add(new StringContent(toFormat), "to_format");

            using var response = await _httpClient.PostAsync("/convert", content);

            if (!response.IsSuccessStatusCode) {
                var error = await response.Content.ReadFromJsonAsync<ApiError>();
                throw new ConversionException(error?.detail ?? $"Error del servidor: {response.StatusCode}");
            }
            return await response.Content.ReadAsByteArrayAsync();
        }
    }

    public class ApiError {
        public string? detail { get; set; }
    }

    public class ConversionException : Exception {
        public ConversionException(string message) : base(message) { }
    }
}
