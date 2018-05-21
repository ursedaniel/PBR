package com.proiect.pbr.vo.convertor;

import com.proiect.pbr.model.Fact;
import com.proiect.pbr.vo.FactVO;
import org.springframework.stereotype.Service;

@Service
public class FactConvertor {

    public FactVO toVO(Fact fact) {
        FactVO factVO = new FactVO();

        factVO.setId(fact.getId());
        factVO.setFact(fact.getFact());

        return factVO;
    }

    public Fact fromVO(FactVO factVO) {
        Fact fact = new Fact();

        fact.setId(factVO.getId());
        fact.setFact(factVO.getFact());

        return fact;
    }
}
