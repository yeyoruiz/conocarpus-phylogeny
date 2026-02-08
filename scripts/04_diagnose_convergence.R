#!/usr/bin/env Rscript
#
# Script para diagnosticar convergencia de análisis BEAST
# Lee archivos .log y genera reportes de convergencia
#
# Uso: Rscript 04_diagnose_convergence.R combretaceae.log
#
# Autor: Análisis Combretaceae
# Fecha: Febrero 2026

# Cargar librerías necesarias
suppressPackageStartupMessages({
  if (!require("coda", quietly = TRUE)) {
    cat("Instalando paquete 'coda'...\n")
    install.packages("coda", repos = "https://cloud.r-project.org")
    library(coda)
  }
  
  if (!require("ggplot2", quietly = TRUE)) {
    cat("Instalando paquete 'ggplot2'...\n")
    install.packages("ggplot2", repos = "https://cloud.r-project.org")
    library(ggplot2)
  }
})

# Función para calcular ESS
calculate_ess <- function(trace) {
  effectiveSize(mcmc(trace))
}

# Función para leer log de BEAST
read_beast_log <- function(file) {
  # Leer archivo saltando comentarios
  lines <- readLines(file)
  
  # Encontrar inicio de datos (después de comentarios #)
  data_start <- which(!grepl("^#", lines))[1]
  
  # Leer datos
  data <- read.table(file, header = TRUE, skip = data_start - 1, 
                     comment.char = "", check.names = FALSE)
  
  return(data)
}

# Función principal
main <- function() {
  args <- commandArgs(trailingOnly = TRUE)
  
  if (length(args) == 0) {
    cat("Error: Se requiere archivo .log\n")
    cat("Uso: Rscript 04_diagnose_convergence.R archivo.log\n")
    quit(status = 1)
  }
  
  log_file <- args[1]
  
  if (!file.exists(log_file)) {
    cat(sprintf("Error: No se encuentra el archivo %s\n", log_file))
    quit(status = 1)
  }
  
  cat("========================================\n")
  cat("  Diagnóstico de Convergencia BEAST\n")
  cat("========================================\n\n")
  
  cat(sprintf("Archivo: %s\n\n", log_file))
  
  # Leer datos
  cat("Leyendo datos...\n")
  data <- read_beast_log(log_file)
  
  n_samples <- nrow(data)
  cat(sprintf("Número de muestras: %d\n\n", n_samples))
  
  # Calcular burnin (25%)
  burnin_n <- ceiling(n_samples * 0.25)
  cat(sprintf("Burnin (25%%): primeras %d muestras\n", burnin_n))
  
  # Datos post-burnin
  data_post <- data[(burnin_n + 1):n_samples, ]
  
  cat("\n========================================\n")
  cat("  Effective Sample Size (ESS)\n")
  cat("========================================\n\n")
  
  # Calcular ESS para cada parámetro
  ess_results <- data.frame(
    Parameter = character(),
    ESS = numeric(),
    Status = character(),
    stringsAsFactors = FALSE
  )
  
  # Excluir columnas no numéricas (Sample, state, etc.)
  numeric_cols <- sapply(data_post, is.numeric)
  
  for (col in names(data_post)[numeric_cols]) {
    if (col %in% c("Sample", "state")) next
    
    trace <- data_post[[col]]
    ess_val <- calculate_ess(trace)
    
    # Determinar status
    if (ess_val >= 200) {
      status <- "✓ OK"
    } else if (ess_val >= 100) {
      status <- "⚠ Bajo"
    } else {
      status <- "✗ Muy bajo"
    }
    
    ess_results <- rbind(ess_results, data.frame(
      Parameter = col,
      ESS = round(ess_val, 1),
      Status = status,
      stringsAsFactors = FALSE
    ))
  }
  
  # Ordenar por ESS
  ess_results <- ess_results[order(ess_results$ESS), ]
  
  # Mostrar resultados
  print(ess_results, row.names = FALSE)
  
  # Resumen
  cat("\n========================================\n")
  cat("  Resumen\n")
  cat("========================================\n\n")
  
  n_ok <- sum(ess_results$ESS >= 200)
  n_low <- sum(ess_results$ESS >= 100 & ess_results$ESS < 200)
  n_very_low <- sum(ess_results$ESS < 100)
  
  cat(sprintf("Parámetros con ESS ≥ 200:    %d / %d (%.1f%%)\n", 
              n_ok, nrow(ess_results), 100 * n_ok / nrow(ess_results)))
  cat(sprintf("Parámetros con ESS 100-199:  %d / %d (%.1f%%)\n", 
              n_low, nrow(ess_results), 100 * n_low / nrow(ess_results)))
  cat(sprintf("Parámetros con ESS < 100:    %d / %d (%.1f%%)\n", 
              n_very_low, nrow(ess_results), 100 * n_very_low / nrow(ess_results)))
  
  # Recomendaciones
  cat("\n========================================\n")
  cat("  Recomendaciones\n")
  cat("========================================\n\n")
  
  if (n_very_low > 0) {
    cat("✗ CONVERGENCIA NO ALCANZADA\n")
    cat("  Acciones recomendadas:\n")
    cat("  1. Extender la corrida (usar -resume en BEAST)\n")
    cat("  2. Aumentar frecuencia de muestreo\n")
    cat("  3. Ajustar operadores (pesos, rangos)\n")
    cat("  4. Simplificar modelo (menos particiones)\n\n")
  } else if (n_low > 0) {
    cat("⚠ CONVERGENCIA MARGINAL\n")
    cat("  Considerar extender la corrida para mayor certeza\n\n")
  } else {
    cat("✓ CONVERGENCIA ALCANZADA\n")
    cat("  Todos los parámetros tienen ESS ≥ 200\n")
    cat("  Puede proceder al análisis post-hoc\n\n")
  }
  
  # Generar gráficos de traces
  cat("Generando gráficos de traces...\n\n")
  
  # Directorio de salida
  output_dir <- "convergence_plots"
  dir.create(output_dir, showWarnings = FALSE)
  
  # Parámetros clave para graficar
  key_params <- c("posterior", "likelihood", "prior", "TreeHeight.t", 
                  "clockRate", "birthRate.t", "deathRate.t")
  
  # Filtrar los que existen
  key_params <- key_params[key_params %in% names(data)]
  
  for (param in key_params) {
    pdf_file <- file.path(output_dir, sprintf("trace_%s.pdf", param))
    
    pdf(pdf_file, width = 10, height = 6)
    
    # Plot con burnin marcado
    plot(data$Sample, data[[param]], type = "l",
         xlab = "Sample", ylab = param,
         main = sprintf("Trace plot: %s", param),
         col = "gray50")
    
    # Línea vertical para burnin
    abline(v = data$Sample[burnin_n], col = "red", lty = 2, lwd = 2)
    
    # Agregar ESS al título
    if (param %in% ess_results$Parameter) {
      ess_val <- ess_results$ESS[ess_results$Parameter == param]
      mtext(sprintf("ESS = %.1f", ess_val), side = 3, line = 0.5, 
            col = ifelse(ess_val >= 200, "darkgreen", "red"))
    }
    
    dev.off()
    
    cat(sprintf("  ✓ %s\n", pdf_file))
  }
  
  # Gráfico de densidad posterior para parámetros clave
  pdf_file <- file.path(output_dir, "posterior_densities.pdf")
  pdf(pdf_file, width = 12, height = 8)
  
  par(mfrow = c(2, 3))
  
  for (param in key_params[1:min(6, length(key_params))]) {
    if (param %in% names(data_post)) {
      dens <- density(data_post[[param]])
      plot(dens, main = param, xlab = "Value", ylab = "Density")
      polygon(dens, col = rgb(0, 0, 1, 0.3), border = NA)
      
      # Agregar media y mediana
      abline(v = mean(data_post[[param]]), col = "red", lwd = 2)
      abline(v = median(data_post[[param]]), col = "blue", lwd = 2, lty = 2)
      
      legend("topright", 
             legend = c(sprintf("Media: %.2f", mean(data_post[[param]])),
                       sprintf("Mediana: %.2f", median(data_post[[param]]))),
             col = c("red", "blue"), lty = c(1, 2), lwd = 2, cex = 0.8)
    }
  }
  
  dev.off()
  cat(sprintf("\n  ✓ %s\n", pdf_file))
  
  # Guardar resumen en archivo
  summary_file <- gsub("\\.log$", "_convergence_summary.txt", log_file)
  
  sink(summary_file)
  cat("========================================\n")
  cat("  Resumen de Convergencia BEAST\n")
  cat("========================================\n\n")
  cat(sprintf("Archivo: %s\n", log_file))
  cat(sprintf("Fecha: %s\n\n", Sys.time()))
  cat(sprintf("Muestras totales: %d\n", n_samples))
  cat(sprintf("Burnin (25%%): %d muestras\n\n", burnin_n))
  cat("\nESS por parámetro:\n\n")
  print(ess_results, row.names = FALSE)
  cat("\n\nResumen:\n")
  cat(sprintf("ESS ≥ 200:    %d / %d (%.1f%%)\n", 
              n_ok, nrow(ess_results), 100 * n_ok / nrow(ess_results)))
  cat(sprintf("ESS 100-199:  %d / %d (%.1f%%)\n", 
              n_low, nrow(ess_results), 100 * n_low / nrow(ess_results)))
  cat(sprintf("ESS < 100:    %d / %d (%.1f%%)\n", 
              n_very_low, nrow(ess_results), 100 * n_very_low / nrow(ess_results)))
  sink()
  
  cat(sprintf("\n✓ Resumen guardado en: %s\n", summary_file))
  
  cat("\n========================================\n")
  cat("  Diagnóstico completado\n")
  cat("========================================\n\n")
}

# Ejecutar
main()
