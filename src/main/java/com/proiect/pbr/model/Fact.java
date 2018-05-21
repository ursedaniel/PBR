package com.proiect.pbr.model;

import javax.persistence.*;

@Entity
@Table(name = "FACTS")
public class Fact {

    private long id;
    private String fact;

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "ID")
    public long getId() {
        return id;
    }
    public void setId(long id) {
        this.id = id;
    }

    @Column(name = "FACT")
    public String getFact() {
        return fact;
    }
    public void setFact(String fact) {
        this.fact = fact;
    }
}
