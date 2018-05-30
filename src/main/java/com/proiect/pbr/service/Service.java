package com.proiect.pbr.service;

import org.springframework.web.multipart.MultipartFile;

public interface Service {
    void storeFile(MultipartFile file);

    boolean runPythonFile(String filename);

    String getFacts(String folder, int i);
}
