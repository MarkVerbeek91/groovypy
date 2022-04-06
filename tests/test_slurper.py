from shlex import shlex
import ast


class GroovySlurper:
    @classmethod
    def parse(cls, string):
        lex = shlex(string)

        return cls.get_token(lex)

    @classmethod
    def get_token(cls, lex):
        try:
            token = next(lex)
        except StopIteration:
            token = None
        else:
            content = cls.get_content(lex)

            if content == "{":
                content = cls.get_token(lex)

            token = {token: content} if content == "}" else token

        return token

    @classmethod
    def get_content(cls, lex):
        try:
            content = next(lex).replace("\"", "")
        except StopIteration:
            content = None
        return content


def slurp(file_content):
    return GroovySlurper.parse(file_content)


def test_slurp_empty_groovy_file_to_emtpy_dict():
    assert slurp("") is None


def test_slurp_groovy_file_with_empty_pipeline():
    file_content = "pipeline"
    assert slurp(file_content) == {"pipeline": None}


def test_slurp_groovy_file_with_variable():
    file_content = "label \"FOO\""
    assert slurp(file_content) == {"label": "FOO"}


def test_slurp_groovy_file_with_variable_brasses():
    file_content = "pipeline {}"
    assert slurp(file_content) == {"pipeline": {}}


# @pytest.mark.skip
def test_slurp_groovy_file_with_pipeline_with_empty_agent():
    file_content = "pipeline { agent }"
    assert GroovySlurper.parse(file_content) == {"pipeline": {"agent": None}}


# @pytest.mark.skip
def test_slurp_groovy_file_with_pipeline_with_agent_defined():
    file_content = """pipeline { agent { label "FOO" } }"""
    assert GroovySlurper.parse(file_content) == dict(pipeline=dict(agent=dict(label="FOO")))


# @pytest.mark.skip
def test_slurp_groovy_file_with_pipeline_with_triggers_defined():
    file_content = """pipeline { triggers { cron('H */6 * * *') } }"""
    assert GroovySlurper.parse(file_content) == {'pipeline': {'triggers': {'cron': 'H */6 * * *'}}}


# @pytest.mark.skip
def test_slurp_groovy_file_with_pipeline_with_stages_defined():
    file_content = """pipeline { stages { } }"""
    assert GroovySlurper.parse(file_content) == {'pipeline': {'stages': {}}}


# @pytest.mark.skip
def test_slurp_groovy_file_with_pipeline_with_stages_with_stage_defined():
    file_content = """layer1 { layer2 { layer3 { } } }"""
    assert GroovySlurper.parse(file_content) == {'layer1': {'layer2': {"layer3": {}}}}


def test_slurp_groovy_file_with_stage_names():
    file_content = """stage('hello') { sh 'foo' }"""
    assert GroovySlurper.parse(file_content) == {"stage": ('hello', {"sh": "foo"})}


def test_slurp_groovy_file_with_stages_with_stage_with_steps_defined():
    file_content = """stages { stage { sh 'foo' } stage { sh 'bar' } }"""
    assert GroovySlurper.parse(file_content) == {"stages": [{"stage": {"sh": "foo"}}, {"stage": {"sh": "bar"}}]}


def test_slurp_groovy_file_with_stages_with_stage_with_names_with_steps_defined():
    file_content = """stages { stage('foo') { sh 'foo' } } stage('bar') { steps { sh 'bar' } }"""
    assert GroovySlurper.parse(file_content) == {
        "stages": [{"stage": ('foo', {"sh": "foo"})}, ('bar', {"stage": {"sh": "bar"}})]}
