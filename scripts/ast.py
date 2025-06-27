from dataclasses import dataclass
from typing import List, Optional, Union

@dataclass
class Program:
    functions: List['Function']

@dataclass
class Function:
    return_type: str
    name: str
    params: List['Param']
    body: List['Statement']

@dataclass
class Param:
    param_type: str
    name: str

@dataclass
class FunctionCall:
    name: str
    args: List[str]

@dataclass
class Expression:
    left: Union[str, 'Expression']
    operator: str
    right: Union[str, 'Expression']

@dataclass
class IfStatement:
    condition: Union[str, Expression]
    true_branch: List['Statement']
    false_branch: Optional[List['Statement']] = None

@dataclass
class WhileStatement:
    condition: Union[str, Expression]
    body: List['Statement']

@dataclass
class Statement:
    value: str
    func_call: Optional[FunctionCall] = None
    if_stmt: Optional[IfStatement] = None
    while_stmt: Optional[WhileStatement] = None
    expression: Optional[Expression] = None
