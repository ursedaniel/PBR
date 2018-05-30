package com.proiect.pbr.controller;

import com.proiect.pbr.service.Service;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@RestController("/clips")
@RequestMapping("/clips")
public class Controller {

    @Autowired
    private Service service;

    @RequestMapping(value = "/upload", method = RequestMethod.POST)
    public void handleFileUpload(@RequestParam("file") MultipartFile file) {

        service.storeFile(file);
    }

    @RequestMapping(value = "/run", method = RequestMethod.GET)
    public boolean runPythonFile(@RequestParam String filename) {

        return service.runPythonFile(filename);
    }

    @RequestMapping(value = "/facts", method = RequestMethod.GET)
    public String getFacts(@RequestParam String folder, @RequestParam int step){
      return service.getFacts(folder, step);
    }

    @RequestMapping(value = "/fact", method = RequestMethod.GET)
    public String getFact(){
        return service.getFact();
    }
}
