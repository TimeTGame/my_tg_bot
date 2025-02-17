from send2trash import send2trash

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import os
# from app.middlewares import TestMiddleware

router = Router()

# router.message.middleware(TestMiddleware())


class files(StatesGroup):
    chdir = State()
    directory = State()
    fileName = State()
    fileContent = State()
    delete = State()

class sec(StatesGroup):
    shutdown = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(f'Hello!\nYour ID: {message.from_user.id}\nName: {message.from_user.full_name}',
                        reply_markup=kb.main)


    
@router.message(F.text == 'Work with files')
async def work_with_files(message: Message):
    await message.answer(f'Current working directory is:\n"{os.getcwd()}"')
    await message.answer('Now you can work with files', reply_markup=kb.kb_files)


@router.callback_query(F.data == 'chdir')
async def chdir_one(callback: CallbackQuery, state: FSMContext):
    await state.set_state(files.chdir)
    await callback.message.edit_text('Write the path to the desired directory')

@router.message(files.chdir)
async def chdir_two(message: Message, state: FSMContext):
    await state.update_data(chdir=message.text)
    data = await state.get_data()

    if os.path.exists(data["chdir"]):
        os.chdir(data["chdir"])
        await message.answer(f'Path successfully changed on:\n"{os.getcwd()}"')
        await message.answer('Now you can work with files', reply_markup=kb.kb_files)
    else:
        await message.answer('This path does not exist')
        await message.answer('Now you can work with files', reply_markup=kb.kb_files)
    
    await state.clear()


@router.callback_query(F.data == 'filesList')
async def filesList(callback: CallbackQuery):
    await callback.message.edit_text(f'List of files in a directory:\n{str(os.listdir(os.getcwd()))}')
    await callback.message.answer('Now you can work with files', reply_markup=kb.kb_files)


@router.callback_query(F.data == 'create')
async def create_choice(callback: CallbackQuery):
    await callback.message.edit_text('Create directory or text file', reply_markup=kb.kb_create)

@router.callback_query(F.data == 'directory')
async def create_question_dir(callback: CallbackQuery, state: FSMContext):
    await state.set_state(files.directory)
    await callback.message.edit_text('Write the desired name for the new directory')

@router.message(files.directory)
async def create_directory(message: Message, state: FSMContext):
    await state.update_data(directory = message.text)
    data = await state.get_data()

    if not os.path.exists(data["directory"]):
        os.makedirs(data["directory"])
        await message.answer(f'Directory {data["directory"]} created')
        await message.answer('Now you can work with files', reply_markup=kb.kb_files)
    else:
        await message.answer('A directory with this name already exists')
        await message.answer('Now you can work with files', reply_markup=kb.kb_files)
    
    await state.clear()


@router.callback_query(F.data == 'textFile')
async def create_question_fileName(callback: CallbackQuery, state: FSMContext):
    await state.set_state(files.fileName)
    await callback.message.edit_text('Write the desired name for the new text file')

@router.message(files.fileName)
async def create_queston_fileContent(message: Message, state: FSMContext):
    await state.update_data(fileName = message.text)
    await state.set_state(files.fileContent)
    await message.answer('Write the desired content for the new text file')

@router.message(files.fileContent)
async def create_textFile(message: Message, state: FSMContext):
    await state.update_data(fileContent = message.text)
    data = await state.get_data()

    if not os.path.exists(data["fileName"]):
        with open(str(data["fileName"]), "w") as file:
            file.write(str(data['fileContent']))
        await message.answer(f'Text file {data["fileName"]} created')
        await message.answer('Now you can work with files', reply_markup=kb.kb_files)
    else:
        await message.answer('A text file with this name already exists')
        await message.answer('Now you can work with files', reply_markup=kb.kb_files)
    
    await state.clear()


@router.callback_query(F.data =='delete')
async def delete_question(callback: CallbackQuery, state: FSMContext):
    await state.set_state(files.delete)
    await callback.message.edit_text('Write the path to the directory or file you want to delete')

@router.message(files.delete)
async def delete_this(message: Message, state: FSMContext):
    await state.update_data(delete = message.text)
    data = await state.get_data()

    if os.path.exists(str(data['delete'])):
        send2trash(str(data["delete"]))
        await message.answer(f'"{str(data["delete"])}"\nhas been deleted')
        await message.answer('Now you can work with files', reply_markup=kb.kb_files)
    else:
        await message.answer(f'"{str(data["delete"])}"\ndoes not exist')
        await message.answer('Now you can work with files', reply_markup=kb.kb_files)



@router.message(F.text == 'Security' or F.text == 'shutdown_No')
async def security(message: Message):
    await message.answer('Now you can play with you computer', reply_markup=kb.kb_security)

@router.callback_query(F.data == 'lock')
async def lock_screen(callback: CallbackQuery):
    await callback.message.edit_text('Your PC is now locked')
    await callback.message.answer('Now you can play with you computer', reply_markup=kb.kb_security)

    os.system("rundll32.exe user32.dll, LockWorkStation")