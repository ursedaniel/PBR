package com.proiect.pbr.service.impl;

import com.proiect.pbr.service.Service;
import org.apache.commons.io.LineIterator;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.multipart.MultipartFile;

import java.io.*;
import java.util.stream.Collectors;

@org.springframework.stereotype.Service
public class ServiceImpl implements Service {

    @Value("${pythonfilepath}")
    private String pythonfilepath;

    @Value("${clipsfilepath}")
    private String clipsfilepath;

    @Value("${outputfilepath}")
    private String outputfilepath;

    @Override
    public void storeFile(MultipartFile file) {

        String fileName = file.getOriginalFilename();
        File newFile = new File(clipsfilepath + fileName);
        try {
            if (!newFile.exists()) {
                newFile.createNewFile();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public boolean runPythonFile(String filename) {
        String[] command = new String[]{"python", pythonfilepath + filename};
        try {
            Process process = Runtime.getRuntime().exec(command);
            return true;

        } catch (Exception e) {
            System.err.println(e);
            return false;
        }
    }

    @Override
    public String getFacts(String folder, int i) {

        File directory = new File(outputfilepath);

        String json = "";

        try {
            File file = new File(outputfilepath+ folder + "\\roteNode" + i + ".txt");
            BufferedReader br = new BufferedReader(new FileReader(file));

            String line;
            while ((line = br.readLine()) != null)
                json += line;

        } catch (Exception e) {
            return e.toString();
        }
        return json;
    }

    @Override
    public String getFact() {
        String json = "";
        try {
            File file = new File(outputfilepath + "\\roteNode.txt");
            BufferedReader br = new BufferedReader(new FileReader(file));

            String line;
            while ((line = br.readLine()) != null)
                json += line;

        } catch (Exception e) {
            return e.toString();
        }
        return json;
    }
}
