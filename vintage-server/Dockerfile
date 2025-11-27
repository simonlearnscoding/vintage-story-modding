# Build stage for the C# mod
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS builder

WORKDIR /app

# Copy project file
COPY VSAPI.csproj ./

# Restore dependencies
RUN dotnet restore

# Copy source code
COPY src/ ./src/

# Build the mod
RUN dotnet build -c Release -o /app/build

# Production stage - create a minimal container with the mod
FROM alpine:latest

# Install necessary runtime dependencies
RUN apk add --no-cache \
    ca-certificates \
    tzdata \
    && rm -rf /var/cache/apk/*

# Create mod directory
WORKDIR /mods

# Copy the built mod from builder stage
COPY --from=builder /app/build /mods/

# Create a simple script to copy mods to Vintage Story server
COPY --from=builder /app/build/VSAPI.dll /mods/VSAPI.dll
COPY modinfo.json /mods/

# The mod will be mounted/copied into the Vintage Story server mods directory
CMD ["/bin/sh"]