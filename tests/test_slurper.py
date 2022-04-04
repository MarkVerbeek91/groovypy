from shlex import shlex
import ast

import pytest


class CustomException(Exception):
    pass


class IsKeyStartError(Exception):
    pass


class IsKeyEndError(Exception):
    pass


class IsDataStartError(Exception):
    pass


class InvalidPairError(Exception):
    pass


class IsDataEndError(Exception):
    pass


class GroovySlurper:

    @classmethod
    def parse(cls, file_data):
        lex = shlex(file_data)

        try:
            content = cls.get_key_content_pair(lex)
        except InvalidPairError:
            content = None
        return content

    @classmethod
    def get_key_content_pair(cls, lex):
        key = cls.get_key(lex)
        content = cls.get_content(lex)

        if key is None and content is None:
            raise InvalidPairError

        return {key: content}

    @classmethod
    def get_key(cls, lex):
        try:
            key = next(lex)
            key = cls.convert_to_type(key)
        except (StopIteration, IsKeyEndError, IsKeyStartError):
            key = None

        return key

    @classmethod
    def get_content(cls, lex):
        try:
            content = next(lex)
        except StopIteration:
            content = None
        else:
            content = cls.process_content(content, lex)
        return content

    @classmethod
    def process_content(cls, content, lex):
        try:
            content = cls.convert_to_type(content)
        except IsKeyStartError:
            try:
                content = cls.get_key_content_pair(lex)
            except InvalidPairError:
                content = {}
        except IsKeyEndError:
            content = None
        except IsDataEndError:
            content = cls.get_key_content_pair(lex)
        except IsDataStartError:
            content = cls.convert_to_type(next(lex))
            try:
                list(next(lex) for _ in range(2))
                # next(lex)
                content = (content, cls.get_key_content_pair(lex))
            except Exception as err:
                print(err)
        return content

    @classmethod
    def convert_to_type(cls, content):
        try:
            content = ast.literal_eval(content)
        except (SyntaxError, ValueError):
            error = {"{": IsKeyStartError,
                     "}": IsKeyEndError,
                     "(": IsDataStartError,
                     ")": IsDataEndError}
            try:
                raise error[content]
            except KeyError:
                pass

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
