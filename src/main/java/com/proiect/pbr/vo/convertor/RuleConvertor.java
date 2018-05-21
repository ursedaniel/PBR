package com.proiect.pbr.vo.convertor;

import com.proiect.pbr.model.Rule;
import com.proiect.pbr.vo.RuleVO;
import org.springframework.stereotype.Service;

@Service
public class RuleConvertor {

    public RuleVO toVO(Rule rule) {
        RuleVO ruleVO = new RuleVO();


        return ruleVO;
    }

    public Rule fromVO(RuleVO ruleVO) {
        Rule rule = new Rule();


        return rule;
    }
}
