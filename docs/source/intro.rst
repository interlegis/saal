Introdução
==========

O SAAL foi desenvolvido com o `Framework Django <https://www.djangoproject.com/>`_,
versão 1.5, utilizando recursos da Interface Administrativa, que acelera o
processo de desenvolvimento e fornece uma interface homogênea,  intuitiva e
fácil de usar.

Ao instalar o SAAL, foi oferecida a opção de se criar um usuário administrador.
Este usuário deve ser utilizado para acessar o sistema sempre que for 
necessário realizar tarefas administrativas, como cadastramento de novos
usuários, alteração de permissões de acesso, exclusão de usuários, modificações
em tabelas administrativas, dentre outros.

O SAAL possui algumas telas genéricas que facilitam o uso do sistema. São elas:

Página do sistema
-----------------

É a página principal do SAAL, apresentada assim que o usuário efetua 
:term:`login`.

.. image:: _static/img/intro/index.png

Esta página possui um cabeçalho, com as boas-vindas ao usuário, e apresenta
todos os módulos que ele tem acesso. Cada aplicação é apresentada em uma caixa
distinta, contendo a sigla, o ícone, o nome, uma breve descrição e
uma lista das principais funcionalidades da aplicação.

Para acessar uma aplicação, pode-se clicar na barra de título da caixa, no ícone
da aplicação, em seu título ou no link *Entrar* na extremidade inferior direita
da caixa.

A página principal do SAAL apresenta ainda uma caixa que relaciona as atividades
recentes realizadas pelos usuários no sistema. Permite que se acesse e
verifique os objetos alterados mais recentemente.

Página de aplicação
-------------------

Ao acessar uma aplicação, é apresentada sua página inicial.

.. image:: _static/img/intro/app_index.png

A página inicial das aplicações possui, logo abaixo da barra de boas-vindas,
uma barra de :term:`menu suspenso`, que permite acessar as suas funcionalidades
de forma rápida e intuitiva.

Logo abaixo da barra de menus, encontra-se a barra de :term:`breadcrumbs`, que
permite visualizar e retornar às partes do sistema já percorridas.

Em seguida vêm o título da aplicação e seu :term:`dashboard`, que dá uma
visão instantânea do desempenho do sistema.